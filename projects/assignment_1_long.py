from dotenv import load_dotenv
import os 
import requests
import json

# load env variable
load_dotenv()

# get the API key from env var
API_KEY = os.getenv('AESO_API_KEY')

url = 'https://api.aeso.ca/report/v1.1/price/poolPrice'

# Define headers
headers = {
    'Accept': 'application/json',
    'X-API-Key': API_KEY
}

# Define the parameters
params = {
    'startDate': '2020-01-01',
    'endDate': ''
}

# API GET request
r = requests.get(url,headers=headers, params=params)

# Parse to a dictionary
response_dict = r.json()

# Check the server response code
print(r.status_code)

# Check the keys in the data
print(response_dict.keys())
print(response_dict)
