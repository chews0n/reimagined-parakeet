import requests
import pandas as pd

class PublicHolidays:
    def __init__(self, country_code):
        self.country_code = country_code

    def get_data(self, year):

        output_file = f'public_holidays{year}.csv'
        try:
            # Make a GET request to the API
            response = requests.get(f'https://date.nager.at/api/v3/PublicHolidays/{year}/{self.country_code}')

            # Check if the request was successful
            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            print ("HTTP Error:",errh)
            return None
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            return None
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            return None
        except requests.exceptions.RequestException as err:
            print ("Something went wrong",err)
            return None

        # Load the response into a DataFrame
        df = pd.DataFrame(response.json())

        # Write the Dataframe to a csv file
        df.to_csv(output_file, index = False)

        return df

# Create an instance of the class for Canada
holidays = PublicHolidays('ca')

# Get public holidays data for the year - 2022
df = holidays.get_data(2023)

# Print the DataFrame
print(list(df.columns), len(df))
print(df)
