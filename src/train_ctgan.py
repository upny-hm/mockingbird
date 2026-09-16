# Hamad Musaid - project Mocking

import pandas as pd
from ctgan import CTGAN


df = pd.read_csv('preprocessed_variable.csv')

# Ensuring categorical columns are read as strings
categorical_cols = ['Account', 'AccountType', 'Computer', 'Task', 'EventID']
for col in categorical_cols:
    df[col] = df[col].astype(str)

print("Training data shape:", df.shape)
print("Discrete columns:", categorical_cols)

# Initializing and training CTGAN
ctgan = CTGAN(epochs=300, verbose=True)
ctgan.fit(df, discrete_columns=categorical_cols)

ctgan.save('ctgan_model.pkl')
print("\nModel trained and saved to ctgan_model.pkl")
