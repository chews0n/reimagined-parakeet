import sys

import pandas as pd

from utils.constants import AESO_API_KEY, BASE_URL, CURRENT_SUPPLY_DEMAND_URL, INTERNAL_LOAD_URL, POOL_PRICE_REPORT, PUBLIC_HOLIDAY_URL
from scrape.aeso_scraper import AESOfetcher
from scrape.weather_canada import DownloadWeatherData
from scrape.public_holiday import Fetch_Public_Holidays 

def main() -> int:
	START_YEAR = 2022
	END_YEAR = 2023 

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
	internal_load_data = fetcher.fetch_data_all_years(INTERNAL_LOAD_URL, START_YEAR, END_YEAR, ["alberta_internal_load"])

	# Fetch Pool Price data for all years
	pool_price_data = fetcher.fetch_data_all_years(POOL_PRICE_REPORT, START_YEAR, END_YEAR, ["pool_price", "rolling_30day_avg"])

	# create a dataframe and lineup the 3 separate headers that you have above with the correct date
	df_headers = ['Date', 'alberta_internal_load', 'pool_price', 'rolling_30day_avg']
	feature_list = pd.DataFrame({
		df_headers[0]: internal_load_data[0],
		df_headers[1]: internal_load_data[1],
		df_headers[2]: pool_price_data[1],
		df_headers[3]: pool_price_data[2]
	})

	print(feature_list.head(10))

	# your feature list will look something like the chart below...
	# Date || alberta_internal_load || pool_price || rolling_30day_avg -> for the headers
	# 2003-01-01 || 98375 || 23.43 || 65.3 --> this will be one row entry
	# ... repeat that for the remaining 20 years

	# check if the dataframe contains nan values
	print(feature_list.isnull().sum())

	for headers in df_headers:
		if feature_list[headers].isnull().sum() > 0:
			# there are nan values, let's handle them programatically
			feature_list[headers].fillna(0.0)

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
	full_date_range = pd.date_range(start=f"{START_YEAR}-01-01", end=f"{END_YEAR}-12-31", freq='D')
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
	weather_downloader = DownloadWeatherData(start_year=START_YEAR, end_year=END_YEAR)
	weather_data = weather_downloader.download_data_to_memory()

	# Extract the relevant columns
	weather_features = weather_data[['Date/Time', 'Mean Temp (°C)', 'Spd of Max Gust (km/h)', 'Total Precip (mm)']].copy()

	# Rename 'Date/Time' to 'Date' for consistency with the existing 'feature_list' DataFrame
	weather_features.rename(columns={'Date/Time': 'Date'}, inplace=True)

	# Merge the weather data with your existing 'feature_list' DataFrame
	feature_list = pd.merge(feature_list, weather_features, on='Date', how='left')

	# Convert column names: lowercase, replace spaces with underscores, remove units in parentheses
	feature_list.columns = (feature_list.columns
						 .str.lower()
						 .str.replace(r"\(.*?\)", "", regex=True)
						 .str.strip()
						 .str.replace(" ", "_"))

	# Check missing values
	feature_list.isnull().sum()
	# Fill missing values with 0.0
	feature_list.fillna(0.0, inplace=True)


	# CREATING NEW FEATURES: Extract the month and the day of the year from the 'date' column
	feature_list['month'] = feature_list['date'].dt.month 
	feature_list['day_of_year'] = feature_list['date'].dt.day_of_year 

	# NEW FEATURES: Previous day’s pool price (float)
	feature_list['previous_day_pool_price'] = feature_list['pool_price'].shift(1).fillna(0) #fill the missing value of the first row

	# Re-arrange columns' positiions
	feature_list = feature_list[['date', 'month', 'day_of_year', 'mean_temp',
							  'spd_of_max_gust', 'total_precip' ,
							  'alberta_internal_load', 'pool_price',
							  'rolling_30day_avg', 'previous_day_pool_price']]
	

	# NEW FEATURES: Public Holidays for Alberta

	# create an instance from public_holiday.py
	holiday_instance = Fetch_Public_Holidays(PUBLIC_HOLIDAY_URL)

	# fetch Alberta holidays and concat to a dataframe
	df_holidays = holiday_instance.fetch_and_combine_holidays(start_year=START_YEAR, end_year=END_YEAR, country='CA')

	# convert 'date' column to datetime type
	df_holidays['date'] = pd.to_datetime(df_holidays['date'])

	# create a new column in the feature list and set all values to 0 initially
	feature_list['is_public_holiday'] = 0

	# Check if the "date" in feature_list exists in df_holidays' "date" column
	# if yes, set the value in "is_public_holiday" column to 1
	feature_list['is_public_holiday'] = feature_list['date'].isin(df_holidays['date']).astype(int)

	# Print the combined DataFrame to check
	print(feature_list.head(10))

	# TODO: Pull down natural gas prices

	return 0


if __name__ == '__main__':
	sys.exit(main())  # next section explains the use of sys.exit
