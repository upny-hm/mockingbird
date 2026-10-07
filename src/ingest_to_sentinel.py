# Hamad Musaid - Project Mockingbird
# Reads synthetic_final.csv from Azure Blob Storage, converts each row to JSON,
# shifts timestamps into a recent window, and sends the records to the
# Log Analytics custom table through the Logs Ingestion API (DCE + DCR).
#
# Usage:
#   python3 ingest_to_sentinel.py --dry-run     # convert only, print sample JSON, send nothing
#   python3 ingest_to_sentinel.py --test        # send the first 10 records
#   python3 ingest_to_sentinel.py               # send all records
#   add --local data/synthetic_final.csv        # read a local file instead of the blob

import argparse
import json
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path

import pandas as pd

# ============================================================
# CONFIGURATION
# ============================================================
STORAGE_ACCOUNT_URL = "https://ctgandataset.blob.core.windows.net"
CONTAINER_NAME = "synthetic-logs"
BLOB_NAME = "synthetic_final.csv"

DCR_ENDPOINT = "https://gan-dce-80tq.qatarcentral-1.ingest.monitor.azure.com"
DCR_IMMUTABLE_ID = "dcr-39010b65e2674b71ada6434fbfd46acd"
STREAM_NAME = "Custom-GAN_CL_CL"


# Left as None unless sign-in picks the wrong directory.
TENANT_ID = None

# Columns to send and their JSON types. Must match the DCR streamDeclarations.
# TenantId is not sent: it is a reserved column that Log Analytics fills itself.
COLUMN_TYPES = {
    "TimeGenerated": "datetime",
    "SourceSystem": "string",
    "Account": "string",
    "AccountType": "string",
    "Computer": "string",
    "EventSourceName": "string",
    "Channel": "string",
    "Task": "int",
    "Level": "string",
    "EventID": "int",
    "Activity": "string",
}

# Timestamps older than 2 days are replaced by Azure with the upload time,
# so the original time range is mapped (keeping order and spacing) into
# the last WINDOW_HOURS, ending a few minutes before now.
WINDOW_HOURS = 24
END_OFFSET_MINUTES = 5

TEST_ROWS = 10
OUTPUT_JSON = Path(__file__).parent / "data" / "synthetic_final.json"


# ============================================================
# LOAD
# ============================================================
def load_csv(local_path, credential):
    if local_path:
        print(f"Reading local file: {local_path}")
        return pd.read_csv(local_path)

    from azure.storage.blob import BlobServiceClient

    print(f"Downloading blob: {CONTAINER_NAME}/{BLOB_NAME}")
    service = BlobServiceClient(account_url=STORAGE_ACCOUNT_URL, credential=credential)
    blob = service.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)
    return pd.read_csv(BytesIO(blob.download_blob().readall()))


# ============================================================
# TRANSFORM: CSV rows -> JSON records
# ============================================================
def shift_timestamps(ts):
    """Map original timestamps linearly into [now - WINDOW_HOURS, now - END_OFFSET]."""
    end = datetime.now(timezone.utc) - timedelta(minutes=END_OFFSET_MINUTES)
    start = end - timedelta(hours=WINDOW_HOURS)
    t_min, t_max = ts.min(), ts.max()
    span = (t_max - t_min).total_seconds() or 1.0
    frac = (ts - t_min).dt.total_seconds() / span
    return pd.to_datetime(start) + pd.to_timedelta(frac * WINDOW_HOURS * 3600, unit="s")


def to_records(df):
    missing = [c for c in COLUMN_TYPES if c not in df.columns]
    if missing:
        raise SystemExit(f"CSV is missing columns: {missing}")

    df = df[list(COLUMN_TYPES)].copy()

    original = pd.to_datetime(df["TimeGenerated"], format="ISO8601", utc=True)
    shifted = shift_timestamps(original)
    print(f"Original time range: {original.min()} -> {original.max()}")
    print(f"Shifted time range:  {shifted.min()} -> {shifted.max()}")

    for col, kind in COLUMN_TYPES.items():
        if kind == "datetime":
            df[col] = shifted.dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        elif kind == "int":
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        else:
            df[col] = df[col].astype("string")

    # JSON has no NaN: missing values become null
    df = df.astype(object).where(df.notna(), None)
    records = df.to_dict(orient="records")
    for r in records:
        for k, v in r.items():
            if hasattr(v, "item"):          # numpy/pandas scalar -> plain Python
                r[k] = v.item()
    return records


# ============================================================
# SEND
# ============================================================
def send(records, credential):
    from azure.monitor.ingestion import LogsIngestionClient

    failed = []

    def on_error(err):
        failed.extend(err.failed_logs)
        print(f"Chunk failed ({len(err.failed_logs)} records): {err.error}")

    client = LogsIngestionClient(endpoint=DCR_ENDPOINT, credential=credential)
    print(f"Sending {len(records)} records to {STREAM_NAME} ...")
    client.upload(rule_id=DCR_IMMUTABLE_ID, stream_name=STREAM_NAME,
                  logs=records, on_error=on_error)
    sent = len(records) - len(failed)
    print(f"Done: {sent} sent, {len(failed)} failed.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="convert only, send nothing")
    parser.add_argument("--test", action="store_true", help=f"send only {TEST_ROWS} records")
    parser.add_argument("--local", help="read this local CSV instead of the blob")
    args = parser.parse_args()

    credential = None
    if not (args.dry_run and args.local):
        from azure.identity import DeviceCodeCredential
        credential = DeviceCodeCredential(tenant_id=TENANT_ID) if TENANT_ID else DeviceCodeCredential()

    df = load_csv(args.local, credential)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    records = to_records(df)

    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(records, indent=2))
    print(f"Saved JSON: {OUTPUT_JSON}")
    print("\nFirst record:\n" + json.dumps(records[0], indent=2))

    if args.test:
        records = records[:TEST_ROWS]

    if args.dry_run:
        print("\nDry run: nothing sent.")
        return

    send(records, credential)


if __name__ == "__main__":
    main()
