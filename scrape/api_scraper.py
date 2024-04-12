import requests


class APIfetcher:
    """A class for fetching data from the an API using API calls"""

    def __init__(self, api_key, base_url, accept_type='application/json'):
        """Initialize the APIfetcher instance"""
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Accept': accept_type,
            'X-API-Key': self.api_key
        }
    
    def fetch_data(self, dataset, params=None):
        """A method to fetch data from a specific dataset.

        dataset: The specific dataset to fetch from the API.
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

    def fetch_data_all_years(self, dataset, start_year, end_year, headers):
        """A method to fetch data all years in the specified range and store it in memory. 
        This will return a list of dictionaries.
        
        dataset: The dataset name to be appended to the base URL mentioned above.
        start_year: The starting year of the range.
        end_year: The ending year of the range.
        """

        # Create an empty list for fetched data
        combined_data = [[] for i in range(len(headers)+1)]

        # Iterate over each year in the range
        for year in range(start_year, end_year+1):
            current_date = f"{year}-01-01"

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

            tmp = [0.0] * len(headers)
            entry_count = 0

            for entry in yearly_data:
                if (entry["begin_datetime_mpt"].split(" ")[0] == current_date):
                    # Average over dailies
                    entry_count += 1
                    for idx, header in enumerate(headers):
                        tmp[idx] += float(entry[header])

                else:
                    combined_data[0].append(current_date)
                    for idx, header in enumerate(headers):
                        combined_data[idx+1].append(tmp[idx]/entry_count)
                    tmp = [0.0] * len(headers)
                    entry_count = 0
                    current_date = entry["begin_datetime_mpt"].split(" ")[0]

                    # Average over dailies
                    for idx, header in enumerate(headers):
                        tmp[idx] += float(entry[header])

            # append the last day to the combined data object
            combined_data[0].append(current_date)
            for idx, header in enumerate(headers):
                combined_data[idx + 1].append(tmp[idx] / entry_count)

        return combined_data
