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


