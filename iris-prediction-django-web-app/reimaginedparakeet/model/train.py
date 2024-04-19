import pandas as pd

from ..utils.constants import *
from ..scrape.api_scraper import APIfetcher
from ..scrape.weather_canada import DownloadWeatherData
from ..scrape.public_holiday import Fetch_Public_Holidays
from ..model.mlModel import MLModel
import _pickle as cPickle


def load_pickle(filename):
	with open(filename, 'rb') as f:
		return cPickle.load(f)

def save_pickle(filename, obj):
	f = open(filename, 'wb')
	cPickle.dump(obj, f, 2)
	f.close()

def train(startyear, endyear, picklefilename):
	if AESO_API_KEY == '':
		print('Please set the AESO_API_KEY environment variable before running the script')
		return 1

	if EIA_API_KEY == '':
		print('Please set the EIA_API_KEY environment variable before running the script')
		return 1

	# Create an instance of the APIfetcher with the API key
	fetcher = APIfetcher(api_key=AESO_API_KEY, base_url=BASE_URL)

	# Fetch Alberta Internal Load data for all years
	internal_load_data = fetcher.fetch_data_all_years(INTERNAL_LOAD_URL, startyear, endyear, ["alberta_internal_load"])

	# Fetch Pool Price data for all years
	pool_price_data = fetcher.fetch_data_all_years(POOL_PRICE_REPORT, startyear, endyear, ["pool_price", "rolling_30day_avg"])

	# create a dataframe and lineup the 3 separate headers that you have above with the correct date
	df_headers = ['Date', 'alberta_internal_load', 'pool_price', 'rolling_30day_avg']
	feature_list = pd.DataFrame({
		df_headers[0]: internal_load_data[0],
		df_headers[1]: internal_load_data[1],
		df_headers[2]: pool_price_data[1],
		df_headers[3]: pool_price_data[2]
	})

	print(feature_list.head(10))

	# check if the dataframe contains nan values
	print(feature_list.isnull().sum())

	for headers in df_headers:
		if feature_list[headers].isnull().sum() > 0:
			# there are nan values, let's handle them programatically
			feature_list[headers].fillna(0.0, inplace=True)

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
	full_date_range = pd.date_range(start=f"{startyear}-01-01", end=f"{endyear}-12-31", freq='D')
	missing_dates = full_date_range.difference(feature_list['Date'])
	print(f"Missing dates are: {missing_dates}")

	# Fetch weather data
	weather_downloader = DownloadWeatherData(start_year=startyear, end_year=endyear)
	weather_data = weather_downloader.download_data_to_memory()

	# Extract the relevant columns
	weather_features = weather_data[
		['Date/Time', 'Mean Temp (°C)', 'Spd of Max Gust (km/h)', 'Total Precip (mm)']].copy()

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
	feature_list['previous_day_pool_price'] = feature_list['pool_price'].shift(1).fillna(
		0)  # fill the missing value of the first row

	# Re-arrange columns' positiions
	feature_list = feature_list[['date', 'month', 'day_of_year', 'mean_temp',
								 'spd_of_max_gust', 'total_precip',
								 'alberta_internal_load', 'pool_price',
								 'rolling_30day_avg', 'previous_day_pool_price']]

	# NEW FEATURES: Public Holidays for Alberta

	# create an instance from public_holiday.py
	holiday_instance = Fetch_Public_Holidays(PUBLIC_HOLIDAY_URL)

	# fetch Alberta holidays and concat to a dataframe
	df_holidays = holiday_instance.fetch_and_combine_holidays(start_year=startyear, end_year=endyear, country='CA')

	# convert 'date' column to datetime type
	df_holidays['date'] = pd.to_datetime(df_holidays['date'])

	# create a new column in the feature list and set all values to 0 initially
	feature_list['is_public_holiday'] = 0

	# Check if the "date" in feature_list exists in df_holidays' "date" column
	# if yes, set the value in "is_public_holiday" column to 1
	feature_list['is_public_holiday'] = feature_list['date'].isin(df_holidays['date']).astype(int)

	# Print the combined DataFrame to check
	print(feature_list.head(10))

	ng_data = APIfetcher(EIA_API_KEY, EIA_BASE_URL)
	ng_params = {'frequency': 'daily', 'data[]': 'value', 'start': f'{startyear - 1}-12-31',
				 'facets[duoarea][]': 'RGC',
				 'end': f'{endyear + 1}-01-31', 'sort[0][column]': 'period', 'sort[0][direction]': 'asc', 'offset': 0,
				 'length': 5000}
	ng_prices, status_code_eia = ng_data.fetch_data(EIA_NATURAL_GAS_URL, params=ng_params)

	# can only grab 5000 entries at a time from the EIA site....
	if len(ng_prices['response']['data']) == 5000:
		# get the maximum date
		max_date = ng_prices['response']['data'][len(ng_prices['response']['data']) - 1]['period']

		ng_params = {'frequency': 'daily', 'data[]': 'value', 'start': max_date,
					 'facets[duoarea][]': 'RGC',
					 'end': f'{endyear + 1}-01-31', 'sort[0][column]': 'period', 'sort[0][direction]': 'asc',
					 'offset': 1,
					 'length': 5000}
		ng_prices2, status_code_eia2 = ng_data.fetch_data(EIA_NATURAL_GAS_URL, params=ng_params)

		ng_prices['response']['data'].extend(ng_prices2['response']['data'])

	feature_list['ng_price'] = 0.0
	ng_idx = 0
	curr_ng_price = ng_prices['response']['data'][ng_idx]['value']

	for index, row in feature_list.iterrows():

		if ng_idx < len(ng_prices['response']['data']):
			while pd.to_datetime(ng_prices['response']['data'][ng_idx]['period']) < row['date']:
				ng_idx += 1

			if pd.to_datetime(ng_prices['response']['data'][ng_idx]['period']) == row['date']:
				curr_ng_price = ng_prices['response']['data'][ng_idx]['value']
				ng_idx += 1

		else:
			print('Range of NG values out of bounds')

		feature_list.loc[index, 'ng_price'] = curr_ng_price

	# build the ML model
	features = ['day_of_year', 'mean_temp', 'spd_of_max_gust', 'total_precip', 'alberta_internal_load',
				'rolling_30day_avg', 'previous_day_pool_price', 'is_public_holiday', 'ng_price']

	elecModel = MLModel(Xvals=feature_list.loc[:, features], Yvals=pd.DataFrame(feature_list.loc[:, 'pool_price']), feature_names=features)

	save_pickle(picklefilename, elecModel)

	#elecModel.plot_feature_importance()

	print(f'Model accuracy is: {elecModel.r2_score}')

	return elecModel.r2_score
