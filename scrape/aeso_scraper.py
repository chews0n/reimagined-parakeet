import requests
import os
import pandas as pd 

class AESOfetcher:
    """A class for fetching data from the AESO API using API calls"""

    def __init__(self, api_key, base_url, accept_type='application/json'):
        """Initialize the AESOfetcher instance"""
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Accept': accept_type,
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
            return None, getattr(e.response, 'status_code', -1)

    def fetch_and_save_data(self, start_year, end_year, dataset, folder_path, file_prefix):
        """A method to fetch and save data for each year in the range of dates.

        start_year: The starting year of the range.
        end_year: The ending year of the range.
        dataset: The dataset name to be appended to the base URL mentioned above.
        folder_path: The folder path to save the CSV files.
        file_prefix: A string added to the start of each saved CSV file's name.
        """
        for year in range(start_year, end_year + 1):
            startDate = f"{year}-01-01"
            endDate = f"{year}-12-31"
            params = {'startDate': startDate, 'endDate': endDate}
            response_data, status_code = self.fetch_data(dataset, params)

            if status_code == -1:
                print(f"The API failed to fetch the data from the request, please look at the API key and the base url being made in the request")
                return status_code
            else:
                print(f"Status Code: {status_code} for year {year}")

            # Determine which dataset we're processing and extract accordingly
            if dataset.endswith('albertaInternalLoad'):
                data = response_data.get('return', {}).get('Actual Forecast Report', [])
            elif dataset.endswith('poolPrice'):
                data = response_data.get('return', {}).get('Pool Price Report', [])
            else:
                data = []

            df = pd.DataFrame(data)  # Convert the list of dictionaries to a pandas DataFrame
            file_name = f"{file_prefix}_{year}.csv"
            full_path = os.path.join(folder_path, file_name)  # Use os.path.join for OS-independent path construction
            df.to_csv(full_path, index=False)  # Export to a CSV file
            print(f"File successfully saved to {full_path}")
