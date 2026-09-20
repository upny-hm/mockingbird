# Hamad Musaid - Project Mockingbird
import pandas as pd
from ctgan import CTGAN

real = pd.read_csv('preprocessed_variable.csv')
ctgan = CTGAN.load('ctgan_model.pkl')

n_samples = 5000
synthetic_data = ctgan.sample(n_samples)

# Resample Account/Computer independently from the real pool
synthetic_data['Account'] = real['Account'].sample(n=n_samples, replace=True).values
synthetic_data['Computer'] = real['Computer'].sample(n=n_samples, replace=True).val>

# Deriving Tsk from EventID - Most common EventID in real Data
# (preserves rare secondary Task values instead of collapsing to the mode)
def sample_task(event_id, real_df):
    options = real_df.loc[real_df['EventID'] == event_id, 'Task']
    if len(options) == 0:
        return None
    return options.sample(n=1, weights=None).values[0]  # uniform draw from that Ev>

synthetic_data['EventID'] = synthetic_data['EventID'].astype(int)
synthetic_data['Task'] = synthetic_data['EventID'].apply(lambda eid: sample_task(ei>


print("Synthetic data shape:", synthetic_data.shape)
print("\nSample rows:\n", synthetic_data.head())
print("\nUnmapped Task:", synthetic_data['Task'].isnull().sum())

synthetic_data.to_csv('synthetic_variable.csv', index=False)
print("\nSaved synthetic_variable.csv")
