# %%
import pandas as pd

# %%
df = pd.read_csv('../dataset/VEVE-raw.csv')

# %%
df.head()

# %%
df.dtypes

# %%
from datetime import datetime
import functools

df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%b %d, %Y'))

# %%
def convert_volume_to_float(vol):
    if vol == '-':
        return 0.0
    else:
        return float(
            vol.replace(',', '')
        )

df['Volume'] = df['Volume'].apply(convert_volume_to_float)

# %%
df = df.sort_values(by='Date')

# %%
df.to_csv('../dataset/VEVE-processed.csv', index=None)

# %%
