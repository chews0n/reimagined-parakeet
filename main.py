import sys
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
	internal_load_data = fetcher.fetch_data_all_years(INTERNAL_LOAD_URL, 2003, 2023)

	# Fetch Pool Price data for all years
	pool_price_data = fetcher.fetch_data_all_years(POOL_PRICE_REPORT, 2003, 2023)

	# Testing: Print first 5 entries of the Alberta Internal Load data
	print("First 5 entries of Alberta Internal Load data:")
	print(internal_load_data[:5])

	# Testing: Print first 5 entries of the Pool Price data
	print("\nFirst 5 entries of Pool Price data:")
	print(pool_price_data[:5])


	# Try fetching Current Supply Demand
	# current_supply_demand, status_code = fetcher.fetch_data(CURRENT_SUPPLY_DEMAND_URL)
	# if status_code == -1:
	# 	print(
	# 		f"The API failed to fetch the data from the request, please look at the API key and the base url being made in the request")
	# 	return status_code
	# else:
	# 	print(f"Status Code: {status_code}")
	# print(current_supply_demand.keys())

	weather_data_downloader = DownloadWeatherData(start_year=2020)
	weather_data_downloader.download_data()

	# TODO: Pull down natural gas prices

	# TODO: Pull down public holidays for Alberta

	return 0


if __name__ == '__main__':
	sys.exit(main())  # next section explains the use of sys.exit
