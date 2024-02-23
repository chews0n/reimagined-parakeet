""" 
Actual Forecarst Data - Batch fetching & exporting

From AESO APIs documentation: "The API will return data for a maximum of 1 year at a time."
So we will fetch the data 1 year at a time. For example, from 2000-01-01 to 2000-12-31, it will be exported to actual_forecast_2000.csv.
Then, we will use the For loop to iterate over the date range that we want.
"""

import sys
from utils.constants import AESO_API_KEY, BASE_URL, CURRENT_SUPPLY_DEMAND_URL, INTERNAL_LOAD_URL, POOL_PRICE_REPORT
from scrape.aeso_scraper import AESOfetcher
import pandas as pd 

def main() -> int:
	# Create an instance of the AESOfetcher with the API key
	fetcher = AESOfetcher(api_key=AESO_API_KEY, base_url=BASE_URL)

	# Loop through the years - Choose the date range that we want
	for year in range(2001, 2010):
		startDate_internal_load = f"{year}-01-01"
		endDate_internal_load = f"{year}-12-31"
		actual_forecast_data, status_code = fetcher.fetch_data(INTERNAL_LOAD_URL,
														   {'startDate': startDate_internal_load, 'endDate': endDate_internal_load})
		print(actual_forecast_data.keys())

		if status_code == -1:
			print(f"The API failed to fetch the data from the request, please look at the API key and the base url being made in the request")
			return status_code
		else:
			print(f"Status Code: {status_code} for year {year}")

		aeso_data = actual_forecast_data['return']['Actual Forecast Report']

		# Convert the list of dictionaries to a pandas DataFrame
		df = pd.DataFrame(aeso_data)

		# Define the folder and filename 
		folder_path = "data/raw"
		file_name = f"actual_forecast_{year}.csv"
		full_path = f"{folder_path}/{file_name}"
		
		# Export to a CSV file
		df.to_csv(full_path, index=False)
		print(f"File succesfully saved to {full_path}")
	
if __name__ == '__main__':
	sys.exit(main())  # next section explains the use of sys.exit
