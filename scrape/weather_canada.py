import urllib.request
from datetime import date
import os


class DownloadWeatherData:

    def __init__(self, station_number=27211, start_year=2010, end_year=date.today().year):
        """

        Initialize the class in order to download the weather data from the Weather Canada website.

        :param station_number: The station number provided by weather canada to extract the data at. The default is
        Calgary Intl CS (27211) for the station id
        :param start_year: The year in which you would like to start the data collection at
        :param end_year: The year you would like to end the data collection at. The default is the current year.
        """

        self.station_number = station_number
        self.start_year = start_year
        self.end_year = end_year

        # This string downloads daily time intervals
        self.scraping_string = "https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID" \
                               "={}&Year={}&Month=1&Day=14&timeframe=2&submit=Download+Data"

    def download_data(self, download_location=os.path.join(os.getcwd(), "weather-data-calgary-{}.csv")):
        """

        This function downloads the daily weather data to the computer in order to extract and work on the data

        :param download_location: The path to the file location that you would like to save the files if you don't
        want them in the current path. Please note that you have to include a {} in the string to differentiate
        between years, otherwise the file will be overwritten and separate files for each year will not be generated
        :return: NULL
        """
        for year in range(self.start_year, self.end_year + 1):
            year_string = self.scraping_string.format(self.station_number, year)
            urllib.request.urlretrieve(year_string, filename=download_location.format(year))
