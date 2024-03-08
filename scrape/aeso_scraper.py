import requests


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

    def fetch_data_all_years(self, dataset, start_year, end_year):
        """A method to fetch data all years in the specified range and store it in memory. 
        This will return a list of dictionaries.
        
        dataset: The dataset name to be appended to the base URL mentioned above.
        start_year: The starting year of the range.
        end_year: The ending year of the range.
        """

        # Create an empty list for fetched data
        combined_data = []

        # Iterate over each year in the range
        for year in range(start_year, end_year+1):
            startDate = f"{year}-01-01"
            endDate = f"{year}-12-31"
            params = {'startDate': startDate, 'endDate': endDate}
            response_data, status_code = self.fetch_data(dataset, params)

            # Check if API call was successful
            if status_code == -1:
                print(f"The API failed to fetch the data from the request, please look at the API key and the base url being made in the request")
                return status_code
            else:
                print(f"Status Code: {status_code} for year {year}")

            # API calls depending on the URL of datasets
            if dataset.endswith('albertaInternalLoad'):
                yearly_data = response_data.get('return',{}).get('Actual Forecast Report',[])
            elif dataset.endswith('poolPrice'):
                yearly_data = response_data.get('return',{}).get('Pool Price Report',[])
            
            # Append the yearly data to the list
            combined_data.extend(yearly_data)

        return combined_data
