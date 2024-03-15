import sys

import pandas as pd

from utils.constants import AESO_API_KEY, BASE_URL, CURRENT_SUPPLY_DEMAND_URL, INTERNAL_LOAD_URL, POOL_PRICE_REPORT
from scrape.aeso_scraper import AESOfetcher
from scrape.weather_canada import DownloadWeatherData

def main() -> int:
	# Create an instance of the AESOfetcher with the API key
	fetcher = AESOfetcher(api_key=AESO_API_KEY, base_url=BASE_URL)


	# Try fetching Actual Forecast for a specific date range
	startDate_internal_load = '2015-01-01'
	endDate_internal_load = '2016-01-01'
	actual_forecast_data, status_code = fetcher.fetch_data(INTERNAL_LOAD_URL,
														   {'startDate': startDate_internal_load, 'endDate': endDate_internal_load})
	print(actual_forecast_data.keys())

	if status_code == -1:
		print(f"The API failed to fetch the data from the request, please look at the API key and the base url being made in the request")
		return status_code
	else:
		print(f"Status Code: {status_code}")

	load_sum = 0.0

	aeso_data = actual_forecast_data['return']['Actual Forecast Report']

	for loadval in range(len(aeso_data)):
		load_sum += float(aeso_data[loadval]['alberta_internal_load'])

	print(f"Total Load for 2015: {load_sum}")


	# Fetch Alberta Internal Load data for all years
	internal_load_data = fetcher.fetch_data_all_years(INTERNAL_LOAD_URL, 2003, 2023, ["alberta_internal_load"])

	# Fetch Pool Price data for all years
	pool_price_data = fetcher.fetch_data_all_years(POOL_PRICE_REPORT, 2003, 2023, ["pool_price", "rolling_30day_avg"])

	# create a dataframe and lineup the 3 separate headers that you have above with the correct date
	feature_list = pd.DataFrame({
		'Date': internal_load_data[0],
		'alberta_internal_load': internal_load_data[1],
		'pool_price': pool_price_data[1],
		'rolling_30day_avg': pool_price_data[2]
	})

	print(feature_list.head(10))

	# your feature list will look something like the chart below...
	# Date || alberta_internal_load || pool_price || rolling_30day_avg -> for the headers
	# 2003-01-01 || 98375 || 23.43 || 65.3 --> this will be one row entry
	# ... repeat that for the remaining 20 years

	# check if the dataframe contains nan values
	print(feature_list.isnull().sum())

	if feature_list.isnull().sum() > 0:
		# there are nan values, let's handle them programatically
		feature_list.fillna(0.0)

		# alternatively you could go through and average entry before and entry afterwards, really most of this is moot
		# but good to have an idea of what to do with missing values.

	# check if all of the dates are present
	# first off, we need to make sure data type of the 'Date' column is datetime:
	print(feature_list['Date'].dtype) 
	# it turns out that this feature is 'Object' which is string.
	# so we have to convert them to datetime format to for next tasks
	feature_list['Date'] = pd.to_datetime(feature_list['Date'])
	# optional: double check the data type, it should be datetime64
	print(feature_list['Date'].dtype) 
	# now we can check the missing dates
	full_date_range = pd.date_range(start='2003-01-01', end='2023-12-31', freq='D')
	missing_dates = full_date_range.difference(feature_list['Date'])
	print(f"Missing dates are: {missing_dates}")

	# check for data that is out of range, if you pull down a temperature was +500*C



	# Try fetching Current Supply Demand
	# current_supply_demand, status_code = fetcher.fetch_data(CURRENT_SUPPLY_DEMAND_URL)
	# if status_code == -1:
	# 	print(
	# 		f"The API failed to fetch the data from the request, please look at the API key and the base url being made in the request")
	# 	return status_code
	# else:
	# 	print(f"Status Code: {status_code}")
	# print(current_supply_demand.keys())

	# weather_data_downloader = DownloadWeatherData(start_year=2020)
	# weather_data_downloader.download_data()

	# Fetch weather data
	weather_downloader = DownloadWeatherData(start_year=2003, end_year=2023)
	weather_data_frames = weather_downloader.download_data_to_memory()

	# Combine all yearly weather data into a single DataFrame
	weather_data_combined = pd.concat(weather_data_frames)

	# Extract the relevant columns
	weather_features = weather_data_combined[['Date/Time', 'Mean Temp (°C)', 'Spd of Max Gust (km/h)', 'Total Precip (mm)']].copy()
	weather_features['Mean Temp (°C)'] = pd.to_numeric(weather_features['Mean Temp (°C)'], errors='coerce')
	weather_features['Spd of Max Gust (km/h)'] = pd.to_numeric(weather_features['Spd of Max Gust (km/h)'], errors='coerce')
	weather_features['Total Precip (mm)'] = pd.to_numeric(weather_features['Total Precip (mm)'], errors='coerce')

	# Rename 'Date/Time' to 'Date' for consistency with the existing 'feature_list' DataFrame
	weather_features.rename(columns={'Date/Time': 'Date'}, inplace=True)

	# Merge the weather data with your existing 'feature_list' DataFrame
	feature_list_with_weather = pd.merge(feature_list, weather_features, on='Date', how='left')

	# Print the combined DataFrame to check
	print(feature_list_with_weather.head(10))

	# TODO: Pull down natural gas prices

	# TODO: Pull down public holidays for Alberta

	return 0


if __name__ == '__main__':
	sys.exit(main())  # next section explains the use of sys.exit
