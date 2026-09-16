import pandas as pd
# Hamad Musaid - Project Mockingbird

# Load dataset
df = pd.read_excel('Sentinel_Training_DataSet.xlsx', sheet_name='Sheet1')

# Save constant columns' values to reattach later
constants = {
    'TenantId': df['TenantId'].iloc[0],
    'SourceSystem': df['SourceSystem'].dropna().iloc[0],
    'EventSourceName': df['EventSourceName'].iloc[0],
    'Channel': df['Channel'].iloc[0] if 'Channel' in df.columns else None,
    'Level': df['Level'].dropna().iloc[0],
}
print("Constants saved:", constants)

# Drop constant + redundant columns
drop_cols = ['TenantId', 'SourceSystem', 'EventSourceName', 'Level', 'Channel', 'Activity']
drop_cols = [c for c in drop_cols if c in df.columns]
df_variable = df.drop(columns=drop_cols)

# Fill missing AccountType with "Unknown" category
df_variable['AccountType'] = df_variable['AccountType'].fillna('Unknown')

# Convert TimeGenerated to numeric (Unix timestamp)

df_variable['TimeGenerated'] = pd.to_datetime(df_variable['TimeGenerated'], format='ISO8601')
df_variable['TimeGenerated_unix'] = df_variable['TimeGenerated'].astype('int64') // 10**9
df_variable = df_variable.drop(columns=['TimeGenerated'])

print("\nRemaining columns:", list(df_variable.columns))
print("\nShape:", df_variable.shape)
print("\nSample:\n", df_variable.head())

# Save for the next step
df_variable.to_csv('preprocessed_variable.csv', index=False)
print("\nSaved preprocessed_variable.csv")
