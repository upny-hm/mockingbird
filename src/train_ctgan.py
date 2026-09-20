# Hamad Musaid - project Mocking

import pandas as pd
from ctgan import CTGAN


# Load preprocessed data, drop unique-ID columns (no real distribution to learn)
df = pd.read_csv('preprocessed_variable.csv')
df_model = df.drop(columns=['Account', 'Computer','Task'])

categorical_cols = ['AccountType', 'EventID']
for col in categorical_cols:
    df_model[col] = df_model[col].astype(str)

print("Training data shape:", df_model.shape)
print("Discrete columns:", categorical_cols)

# batch_size= 50 meaningfully more gradient updates per epoch on this small dataset>
# Increased epochs=800 to compensate for smaller batches with more training passes.
ctgan = CTGAN(epochs=800, batch_size=50, verbose=True)
ctgan.fit(df_model, discrete_columns=categorical_cols)

ctgan.save('ctgan_model.pkl')
print("\nModel trained and saved to ctgan_model.pkl")
