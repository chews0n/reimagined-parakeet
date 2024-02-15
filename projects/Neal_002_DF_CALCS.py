# %%
import pandas as pd
import numpy as np  # We might need NumPy for smoothing
import matplotlib.pyplot as plt
import plotly.express as px  # For easy Plotly graph creation
from datetime import datetime, timedelta
import os

data_path = "../data/raw/SystemMarginalPrice_6M0.csv"
df = pd.read_csv(data_path, parse_dates=['begin_datetime_mpt', 'end_datetime_mpt', 'end_datetime_utc', 'begin_datetime_utc'])
print(df.dtypes)
print(df.head())

# %%
# Rename columsn
df.rename(columns={'system_marginal_price': 'price'}, inplace=True)


df['price_per_volume'] = df['volume'] / df['price']
df['duration'] = df['end_datetime_mpt'] - df['begin_datetime_mpt']
df['duration_seconds'] = df['duration'].dt.total_seconds()
df['duration_minutes'] = df['duration'].dt.total_seconds() / 60
df['rate_per_hour'] = df['volume'] / df['duration_minutes'] /60
df['cost'] = df['volume'] * df['price']
df['month'] = df['begin_datetime_mpt'].dt.month  # Or use another timestamp column


print(df.head())

# CSV Export ------------------------------------------------------------
output_folder = "../data/interim/"  # Go back one folder, then into 'data/raw'
output_filename = "SystemMarginalPrice_6M0_ADDCOLS.csv"
output_path = os.path.join(output_folder, output_filename)

# Ensure the output folder exists, its a new interim one
os.makedirs(output_folder, exist_ok=True)

df.to_csv(output_path, index=False)  # Save CSV without index column
print(f'File output to {output_path}')

# Create the Plotly figure for Volume Trend------------------------------
fig = px.line(df, x='begin_datetime_mpt', y='volume', title='Volume Trend')

# Create the Plotly figure for Volume Trend------------------------------
fig = px.line(df, x='begin_datetime_mpt', y='rate_per_hour', title='Volume Trend')

# Customize (optional)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Rate"
)

fig.show()
        
# Create the Plotly figure For Price
fig = px.line(df, x='begin_datetime_mpt', y='price_per_volume', title='Price Trend')

# Customize (optional)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price"
)

fig.show()

# Create the Plotly figure For Cost
fig = px.line(df, x='begin_datetime_mpt', y='cost', title='Cost Trend')

# Customize (optional)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Cost"
)

fig.show()

monthly_costs = df.groupby('month')['cost'].sum()
print(monthly_costs)

import plotly.express as px

fig = px.bar(monthly_costs, x=monthly_costs.index, y='cost', 
             title='Monthly Electricity Costs')
fig.show()
