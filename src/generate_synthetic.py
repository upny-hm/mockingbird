# Hamad Musaid - Project Mockingbird

import pandas as pd
from ctgan import CTGAN

# Load trained model
ctgan = CTGAN.load('ctgan_model.pkl')

# Generate synthetic rows (5000)
n_samples = 5000
synthetic_data = ctgan.sample(n_samples)

print("Synthetic data shape:", synthetic_data.shape)
print("\nSample rows:\n", synthetic_data.head())

synthetic_data.to_csv('synthetic_variable.csv', index=False)
print("\nSaved synthetic_variable.csv")
