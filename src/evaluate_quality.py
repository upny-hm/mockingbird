# Hamad Musaid - Project Mockingbird 


import pandas as pd
from sdmetrics.reports.single_table import QualityReport
from sdv.metadata import SingleTableMetadata

# Evaluate only the CTGAN-modeled columns (Account/Computer excluded by design)
# task also removed since Task is derived from EventID not what CTGAN models
model_cols = ['AccountType', 'EventID', 'TimeGenerated_unix']

real = pd.read_csv('preprocessed_variable.csv')[model_cols]
synth = pd.read_csv('synthetic_variable.csv')[model_cols]

categorical_cols = ['AccountType', 'EventID']
for col in categorical_cols:
    real[col] = real[col].astype(str)
    synth[col] = synth[col].astype(str)

metadata = SingleTableMetadata()
metadata.detect_from_dataframe(real)

report = QualityReport()
report.generate(real, synth, metadata.to_dict())

print("\nOverall Quality Score:", report.get_score())
print("\nProperty breakdown:")
print(report.get_properties())
