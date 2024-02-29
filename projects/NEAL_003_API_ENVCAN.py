# %%
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from dateutil import rrule
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import re

# We'll need `fuzzywuzzy` to look up weather stations later
# Run "!pip install fuzzywuzzy --user" if you get an error

# !pip install fuzzywuzzy --user
from fuzzywuzzy import fuzz


##How to download one month of data:

month = "01" # January
year = "2020" # 2020
stationID = 50430 #Calgary

base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
api_endpoint = base_url + query_url

print("Click me to download CSV data:")
print(api_endpoint)
# %%

# Call Environment Canada API
# Returns a dataframe of data
def getHourlyData(stationID, year, month):
    base_url = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?"
    query_url = "format=csv&stationID={}&Year={}&Month={}&timeframe=1".format(stationID, year, month)
    api_endpoint = base_url + query_url
    return pd.read_csv(api_endpoint, skiprows=0)

# %%
stationID = 50430
year = 2015
month = 6 

df = getHourlyData(stationID, year, month) 
#print(df.head()) 
print(df.columns) 
# %%

stationID = 50430
start_date = datetime.strptime('Jun2020', '%b%Y')
end_date = datetime.strptime('Jun2023', '%b%Y')


frames = []
for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
    df = getHourlyData(stationID, dt.year, dt.month)
    frames.append(df)

weather_data = pd.concat(frames)
weather_data['Date/Time (LST)'] = pd.to_datetime(weather_data['Date/Time (LST)'])
weather_data['Temp (°C)'] = pd.to_numeric(weather_data['Temp (°C)'])
# %%  ------just an example call

df = getHourlyData(stationID, 2023, 6) # Example call
print(df.head())

# %%