# Hamad Musaid - Project Mockingbird
# Format validation: checks IPs, usernames and timestamps in the synthetic data
# against the same structural rules applied to the original dataset.

import re
import ipaddress
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent
real = pd.read_excel(BASE / 'Sentinel_Training_DataSet.xlsx', sheet_name='Sheet1')
synth = pd.read_csv(BASE / 'data' / 'synthetic_final.csv')


def is_ip(value):
    try:
        ipaddress.ip_address(str(value))
        return True
    except ValueError:
        return False


def is_account(value):
    return re.fullmatch(r'Account\d+', str(value)) is not None


def is_timestamp(value):
    return re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z', str(value)) is not None


checks = {
    'Computer (valid IP)': ('Computer', is_ip),
    'Account (Account<number>)': ('Account', is_account),
    'TimeGenerated (ISO 8601 Z)': ('TimeGenerated', is_timestamp),
}

print(f"{'Check':30}{'Original':>12}{'Synthetic':>12}")
all_pass = True
for name, (col, fn) in checks.items():
    real_pct = real[col].dropna().map(fn).mean() * 100
    synth_pct = synth[col].map(fn).mean() * 100
    all_pass &= synth_pct == 100.0
    print(f"{name:30}{real_pct:11.1f}%{synth_pct:11.1f}%")

nulls = int(synth[['Computer', 'Account', 'TimeGenerated']].isnull().sum().sum())
print(f"\nSynthetic rows: {len(synth)} | Nulls in checked columns: {nulls}")
print('RESULT:', 'PASS (100% structural match)' if all_pass and nulls == 0 else 'FAIL')
