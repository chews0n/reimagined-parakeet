import requests
import pandas as pd
import json

import numpy as np


class APIDataFetcher:

    def __init__(self, url, headers, api_key):
        self.url = url
        self.headers = headers
        self.api_key = api_key

    def fetch_data(self, start_date, end_date):
        url_with_key = f"{self.url}?api_key={self.api_key}"

        self.headers["X-Params"] = json.dumps({
            "frequency": "daily",
            "data": ["value"],
            "facets": {},
            "start": start_date,
            "end": end_date,
            "sort": [{"column": "period", "direction": "desc"}],
            "offset": 0,
            "length": 5000
        })

        response = requests.get(url_with_key, headers=self.headers)
        data = response.json()
        return data
    

    def save_as_csv(self, data):
        simplified_data = [{'date': item['period'], 'price': item['value']} for item in data['response']['data']]
        df = pd.DataFrame(simplified_data)
        return df

# Usage
url = "https://api.eia.gov/v2/natural-gas/pri/fut/data/"
headers = {
    "X-Params": json.dumps({
        "frequency": "daily",
        "data": ["value"],
        "facets": {},
        "start": "2000-01-01",
        "end": "2000-12-31",
        "sort": [{"column": "period", "direction": "asc"}],
        "offset": 0,
        "length": 5000
    })
}
api_key =  "80YB0XgTZLn682y6ggfsh4Q8Vy4GGyqt8YgdCFbR"     # API key
fetcher = APIDataFetcher(url, headers, api_key)

# Create an empty DataFrame
all_data = pd.DataFrame()

# Loop over the years
for year in range(2023, 1999, -1):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    data = fetcher.fetch_data(start_date, end_date)
    yearly_data = fetcher.save_as_csv(data)
    all_data = all_data.append(yearly_data, ignore_index=True)

# Save all data to a CSV file in data/raw folder
all_data.to_csv("data/raw/all_Nat_gas_prices.csv", index=False)

# ---------------------------*---------------------------------------------------

# to get average price for each date and save the data to a csv
all_data['date']= pd.to_datetime(all_data['date'])
all_data['price'] = all_data['price'].astype(float)

# Group by 'date' and calculate the mean of 'price'
all_data_avg = all_data.groupby('date')['price'].mean()

# Round the mean to 3 decimal places
all_data_avg_rounded = all_data_avg.round(3).reset_index()

# Save the result to a new csv file
all_data_avg_rounded.to_csv('data/raw/all_NatGasPrices_daily_avg.csv', index = False)

