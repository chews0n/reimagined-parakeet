import requests
import pandas as pd

# URL of the dataset
url = 'https://datahub.io/vara.maruboina/henry-hub-natural-gas-spot-price/r/0.csv'

try:
    # Send HTTP request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful

    # Save the content to a file
    with open('henry_hub_natural_gas_spot_price.csv', 'w') as file:
       file.write(response.text)

    # Load the data into a DataFrame
    df = pd.read_csv('henry_hub_natural_gas_spot_price.csv')
    
	# Define the folder and filename 
    folder_path = "data/raw"
    file_name = "henry_hub_natural_gas_spot_price.csv"
    full_path = f"{folder_path}/{file_name}"
	
	# Export to a CSV file
    df.to_csv(full_path, index=False)
    print(f"File succesfully saved to {full_path}")
        


except requests.exceptions.RequestException as e:
    print(f"An error occurred while trying to get the data: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")# Send HTTP request to the URL
response = requests.get(url)


	

# Print the first few rows of the DataFrame
print(df.head())
print(len(df))
print(df.Date.max(), df.Date.min())