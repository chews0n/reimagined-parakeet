import requests
import json

from utils.constants import AESO_API_KEY, BASE_URL, CURRENT_SUPPLY_DEMAND_URL, INTERNAL_LOAD_URL, POOL_PRICE_REPORT, CALGARY_API_URL
from scrape.aeso_scraper import AESOfetcher
from scrape.weather_canada import DownloadWeatherData
from scrape.public_holiday import Fetch_Public_Holidays

# No need to copy/paste the class and constants into here, that's what imports are for

# Create an instance of the AESOfetcher with the API key
fetcher = AESOfetcher(api_key=AESO_API_KEY,base_url=BASE_URL)

# Try fetching Actual Forecast for a specific date range

actual_forecast_data, status_code = fetcher.fetch_data(INTERNAL_LOAD_URL,
                                        {'startDate':'2015-01-01', 'endDate':'2016-01-01'})
print(actual_forecast_data.keys())
print(f"Status Code: {status_code}")

# Try fetching Current Supply Demand
current_supply_demand, status_code = fetcher.fetch_data(CURRENT_SUPPLY_DEMAND_URL)
print(f"Status Code: {status_code}")
print(current_supply_demand.keys())

load_sum = 0.0
aeso_data = actual_forecast_data['return']['Actual Forecast Report']
for loadval in range(len(aeso_data)):
		load_sum += float(aeso_data[loadval]['alberta_internal_load'])

print(f"Total Load for 2015: {load_sum}")

# Try fetching Pool Price Report
pool_price_rep, status_code = fetcher.fetch_data(POOL_PRICE_REPORT,
                                        {'startDate':'2015-01-01', 'endDate':'2016-01-01'})
print(f"Status Code: {status_code}")
print(pool_price_rep.keys())

# Create an instance of the Calgary API with the API key
#yyc_fetcher = AESOfetcher(api_key=AESO_API_KEY,base_url=CALGARY_API_URL)
#
# # Try fetching Actual Forecast for a specific date range
#
# yyc_forecast_data, status_code = yyc_fetcher.fetch_data('citypage_weather/xml/AB/s0000047_e.xml'  ,
#                                         {'startDate':'2015-01-01', 'endDate':'2016-01-01'})

# You're trying to download from an xml file here, you can't just request stuff from any website, there needs to be a gateway to grab stuff. In this case, it looks like you're just trying to download a file, I've added a class that does this for you in the weather_canada.py file by making a url request over a date range.

# This will download the weather data into
weather_data = DownloadWeatherData()
weather_data.download_data()

#This will create an instance of the Public Holiday fetcher
PH_fetcher = Fetch_Public_Holidays(base_url=PUBLIC_HOLIDAY_URL)

# This will fetch the data, provided year and country
PH_data = PH_fetcher.fetch_data('2024','CA')

for public_holiday in public_holidays:
  print(public_holiday['date'], public_holiday['name'], public_holiday['types'])

