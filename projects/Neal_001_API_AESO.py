# junk
# %%
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px  # For easy Plotly graph creation
from datetime import datetime, timedelta
import os

# %%
AESO_API_KEY='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ4bGs2dTYiLCJpYXQiOjE3MDc1MDYwOTZ9.JtX8AnzuRpMBMibDs5q7oaEzH9etllM_xWGtS-qbv0Q'

def get_smp_trend(start_date, end_date, api_key=AESO_API_KEY):
    """Fetches and visualizes the System Marginal Price (SMP) trend.

    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        api_key (str, optional): Your AESO API key.
    """

    url = "https://api.aeso.ca/report/v1.1/price/systemMarginalPrice"
    params = {
        "startDate": start_date,
        "endDate": end_date,
    }
    headers = {
        "X-API-Key": AESO_API_KEY  # Include the API key in the 'X-API-Key' header 
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        #data = response.json() 
        #print(data)  # Add this line 
        data = response.json()["return"]["System Marginal Price Report"]

        df = pd.DataFrame(data)
        # Convert datetime columns if needed
        if 'begin_datetime_mpt' in df.columns:  # Adjust column name if necessary
            df['begin_datetime_mpt'] = pd.to_datetime(df['begin_datetime_mpt'])
            
        if 'volume' in df.columns:  # Adjust column name if necessary
            df['volume'] = pd.to_numeric(df['volume'])
            
        if 'system_marginal_price' in df.columns:  # Adjust column name if necessary
            df['system_marginal_price'] = pd.to_numeric(df['system_marginal_price'])
        
        # CSV Export ------------------------------------------------------------
        output_folder = "../data/raw/"  # Go back one folder, then into 'data/raw'
        output_filename = "SystemMarginalPrice_6M0.csv"
        output_path = os.path.join(output_folder, output_filename)

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        df.to_csv(output_path, index=False)  # Save CSV without index column
        print(f'File output to {output_path}')
        # Create the Plotly figure for Volume Trend------------------------------
        fig = px.line(df, x='begin_datetime_mpt', y='volume', title='Volume Trend')

        # Customize (optional)
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Volume"
        )

        fig.show()
                
        # Create the Plotly figure For Price
        fig = px.line(df, x='begin_datetime_mpt', y='system_marginal_price', title='Price Trend')

        # Customize (optional)
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price"
        )

        fig.show()

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
    except requests.exceptions.HTTPError as e:
        # Handle specific HTTP error codes here
        if e.response.status_code == 400:
            print("Bad request. Please check your parameters.")
        elif e.response.status_code == 401:
            print("Unauthorized. Please check your API key.")
        elif e.response.status_code == 403:
            print("Forbidden. You may not have access to this resource.")
        elif e.response.status_code == 404:
            print("Not found. The specified resource may not exist.")
        elif e.response.status_code == 405:
            print("Invalid method. Please check the allowed HTTP methods.")
        elif e.response.status_code == 500:
            print("Internal server error. Please try again later.")
        elif e.response.status_code == 503:
            print("Service unavailable. Please try again later.")
        else:
            print(f"Unexpected HTTP error: {e.response.status_code}")

# %%
# Assinged Dates
start_date = "2023-08-05"
end_Date = "2024-01-01"
# Calculate today's date
today = datetime.today()   

# Calculate start date (6 months prior)
start_date = today - timedelta(days=30*6)  # Approximately 6 months
start_date = start_date.strftime('%Y-%m-%d')  # Format for API request
end_date = datetime.today().date().strftime('%Y-%m-%d')
get_smp_trend(start_date, end_date)

# %% -------------------------  END ------------------------------


