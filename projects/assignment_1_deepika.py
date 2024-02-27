import requests
import pandas as pd
import sys
import os 

#from utils.constants import AESO_API_KEY, BASE_URL, CURRENT_SUPPLY_DEMAND_URL, INTERNAL_LOAD_URL, POOL_PRICE_REPORT
BASE_URL='https://api.aeso.ca/report'
CURRENT_SUPPLY_DEMAND_URL='v1/csd/summary/current'
INTERNAL_LOAD_URL='v1/load/albertaInternalLoad'
POOL_PRICE_REPORT='v1.1/price/poolPrice'
CALGARY_API_URL='https://api.weather.gc.ca/'

API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxaGdybnIiLCJpYXQiOjE3MDg4MzQ2MTB9.araoxmr54HxheygYczjrBdExAW-QhaQS-cl09IzMZ_k'

class AESO_dataScrape:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = BASE_URL  #'https://api.aeso.ca/report'
        self.headers = {
                'accept': 'application/json',
                'X-API-Key': self.api_key
            }

    def fetch_and_write_tocsv(self, dataset, year):
        if dataset.strip().lower() == 'pool_price_report':
            dataset_url =  POOL_PRICE_REPORT     #'v1.1/price/poolPrice'
            output_csv_file = f'pool_price{year}.csv'    # define the csv_file based on year and report requested
            report_type = 'Pool Price Report'

        elif dataset.strip().lower() == 'actual_forecast_report':
            dataset_url =  INTERNAL_LOAD_URL      #'v1/load/albertaInternalLoad'
            output_csv_file = f'actual_forecast{year}.csv'
            report_type = 'Actual Forecast Report'

        try:
            date_url = f'?startDate={year}-01-01&endDate={year}-12-31'
        

            # Define the API endpoint
            url = f'{self.base_url}/{dataset_url}{date_url}'

            # Send a GET request to the API
            response = requests.get(url, headers = self.headers)

            # Raise an exception if the request was unsuccessful
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the report: {e}")
            return None

        # Convert the response to JSON
        data = response.json()

        # Convert the JSON data to a pandas DataFrame
        df = pd.DataFrame(data['return'][report_type])

        # Define the folder and filename 
        folder_path = "data/raw"
        file_name = output_csv_file
        full_path = f"{folder_path}/{file_name}"
        
        # Write the DataFrame to a CSV file
        df.to_csv(full_path, index=False)
        print(f"File succesfully saved to {full_path}")

        return df

# Create an instance of the class
report = AESO_dataScrape(API_KEY)

# Fetch the required data_report for the required year and write it to a CSV file
# choose 'actual_forecast_report' or 'pool_price_report' and year
df = report.fetch_and_write_tocsv('actual_Forecast_report',2001)
df = report.fetch_and_write_tocsv('pool_price_report', 2001 )

# Print the DataFrame
print(df)

