# Hamad Musaid - Project Mockingbird

import pandas as pd

# Load original data (for EventID -> Activity mapping) and synthetic data
original = pd.read_excel('Sentinel_Training_DataSet.xlsx', sheet_name='Sheet1')
synth = pd.read_csv('synthetic_variable.csv')

# Build EventID -> Activity lookup from original data
event_activity_map = original.drop_duplicates('EventID').set_index('EventID')['Activity'].to_dict()

# Reattach constant columns
synth['TenantId'] = '6618e8e6-0ec0-4001-9280-a9835bdbd933'
synth['SourceSystem'] = 'OpsManager'
synth['EventSourceName'] = 'Microsoft-Windows-Security-Auditing'
synth['Channel'] = 'Security'
synth['Level'] = 0.0

# Rebuild Activity from EventID
synth['Activity'] = synth['EventID'].map(event_activity_map)

# Convert TimeGenerated_unix back to Sentinel's ISO8601 string format
synth['TimeGenerated'] = pd.to_datetime(synth['TimeGenerated_unix'], unit='s').dt.strftime('%Y-%m-%dT%H:%M:%S.0000000Z')
synth = synth.drop(columns=['TimeGenerated_unix'])

# Reorder columns to match the original schema
final_cols = [c for c in original.columns if c in synth.columns]
synth_final = synth[final_cols]

print("Final columns:", list(synth_final.columns))
print("Shape:", synth_final.shape)
print("\nUnmapped Activity (should be 0):", synth_final['Activity'].isnull().sum())
print("\nSample:\n", synth_final.head())

synth_final.to_csv('synthetic_final.csv', index=False)
print("\nSaved synthetic_final.csv")
