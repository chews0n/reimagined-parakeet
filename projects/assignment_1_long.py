from dotenv import load_dotenv
import os 
import requests
import json

# Load environment variables from a .env file
load_dotenv()

# Get the API key
API_KEY = os.getenv('AESO_API_KEY')

class AESOfetcher:
    """A class for fetching data from the AESO API using API calls"""

    def __init__(self, api_key):
        """Initialize the APIfetcher instance"""
        self.api_key = api_key
        self.base_url = 'https://api.aeso.ca/report'
        self.headers = {
            'Accept': 'application/json',
            'X-API-Key': self.api_key
        }
    
    def fetch_data(self, dataset, params=None):
        """A method to fetch data from a specific dataset.

        dataset: The specific dataset to fetch from the AESO API.
        params: An optional dictionary of parameters for the query (e.g. startDate).
        """
        try:
            url = f"{self.base_url}/{dataset}"
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()     # This will raise an HTTPError for bad responses
            return response.json(), response.status_code
        except requests.RequestException as e:
            print(f"Error fetching  data: {e}")
            return None, getattr(e.response, 'status_code', 0)

# Create an instance of the APIfetcher with the API key
fetcher = AESOfetcher(api_key=API_KEY)

# Try fetching Actual Forecast for a specific date range
actual_forecast_data, status_code = fetcher.fetch_data('v1/load/albertaInternalLoad', 
                                        {'startDate':'2015-01-01', 'endDate':'2016-01-01'})
print(actual_forecast_data.keys())
print(f"Status Code: {status_code}")

# Try fetching Current Supply Demand
current_supply_demand, status_code = fetcher.fetch_data('v1/csd/summary/current')
print(f"Status Code: {status_code}")
print(current_supply_demand.keys())