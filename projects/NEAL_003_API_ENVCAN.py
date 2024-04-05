# %%
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
from dateutil import rrule
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re

'''
# We'll need `fuzzywuzzy` to look up weather stations later
# Run "!pip install fuzzywuzzy --user" if you get an error
# !pip install fuzzywuzzy --user
from fuzzywuzzy import fuzz
'''
output_dir = '..\\data\\interim'

##How to download one month of data:

month = "01" # January
year = "2020" # 2020
stationID = 50430 #Calgary

base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
api_endpoint = base_url + query_url

# I like this little trick
print("Click me to download CSV data:")
print(api_endpoint)
# %%

# Call Environment Canada API
# Returns a dataframe of data
def getHourlyData(stationID, year, month):
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    query_url = f"format=csv&stationID={stationID}&Year={year}&Month={month}&timeframe=1"
    api_endpoint = base_url + query_url
    return pd.read_csv(api_endpoint, skiprows=0)

# %%
stationID = 50430
year = 2015
month = 6 
# run teh function to get the dataframe
df = getHourlyData(stationID, year, month) 
#print(df.head()) 
print(df.columns) 
# %%

stationID = 50430 # Calgary
start_date = datetime.strptime('Jun2012', '%b%Y')
end_date = datetime.strptime('Jun2023', '%b%Y')

frames = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    df = getHourlyData(stationID, dt.year, dt.month)
    frames.append(df)

weather_data = pd.concat(frames)
weather_data['Date/Time (LST)'] = pd.to_datetime(weather_data['Date/Time (LST)'])
weather_data['Temp (°C)'] = pd.to_numeric(weather_data['Temp (°C)'])

# %%
print(weather_data.columns)
print(weather_data.head(2))
# %%

# Create a Plotly figure
fig = go.Figure()

# Add a trace for temperature vs. date
fig.add_trace(go.Scatter(x=weather_data['Date/Time (LST)'], y=weather_data['Temp (°C)'],
                         mode='lines',
                         name='Temperature (°C)'))

# Update layout for better readability
fig.update_layout(
    title="Calgary Temperature Over Time",
    xaxis_title="Date",
    yaxis_title="Temperature (°C)",
    template="plotly_white"  # Use white background
)

# Show the plot
fig.show()

# Export the data to csv
weather_data.to_csv(os.path.join(output_dir, 'all_years_weather_data_envcan.csv')) 


# %%  ------just an example call, to see what it does

df = getHourlyData(stationID, 2023, 6) # Example call
print(df.head())

# %%
