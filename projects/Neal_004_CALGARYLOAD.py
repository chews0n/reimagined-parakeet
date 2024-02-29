'''
This file will load the excel files and create a single CSV of Edmonton and Calgary power Usage

We can then use the Enviro Canada Calgary and Edmonton weather to do a better trend

Does AESO API have power usage by Region or City?

'''
# %%
import os
import glob
import pandas as pd

def load_excel_files(folder_path, file_pattern, sheet_name, datetime_column):
    """
    Loads multiple Excel files with a specific pattern into a single DataFrame

    Args:
        folder_path (str): The path to the folder containing the Excel files.
        file_pattern (str): The pattern to match in the Excel filenames.
        sheet_name (str): The name of the sheet to load from each Excel file.
        datetime_column (str): The name of the column to parse as a date.

    Returns:
        pandas.DataFrame: A DataFrame containing the combined data from all matching Excel files.
    """
    all_data = []  # Initialize an empty list to store DataFrame objects

    # Get the list of Excel files matching the pattern
    file_path = os.path.join(folder_path, file_pattern)
    excel_files = glob.iglob(file_path)  # Use glob to find files matching the pattern

    # Loop through each file and load data into a DataFrame
    for file in excel_files:
        df = pd.read_excel(file, 
                           sheet_name=sheet_name, 
                           header=0,  
                           skiprows=1, 
                           parse_dates=[datetime_column],
                           date_format='%Y-%m-%d %H:%M:%S')  # Specify date format if applicable
        all_data.append(df)  # Append the DataFrame to the list

    return pd.concat(all_data, ignore_index=True)  # Concatenate all DataFrames into a single DataFrame


# ---  Usage ---
folder_path = '..\\data\\raw'
file_pattern = "Hourly*.xlsx"
sheet_name = 'Load by AESO Planning Area'
datetime_column = 'DATE_TIME'

df = load_excel_files(folder_path, file_pattern, sheet_name, datetime_column)

print(df)


# %% ------------------EXPORT DF to csv in interim------------------
# Create the 'interim' folder if it doesn't exist
os.makedirs('..\\data\\interim', exist_ok=True)
print('directory made')

# Export to CSV
df.to_csv('..\\data\\raw\\combined_AESO_load-by-area.csv', index=False) 
print('File written to raw')

# %%
