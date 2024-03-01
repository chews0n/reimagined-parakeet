# Project 1: Creating and using a class to make an API request to the AESO API

1. Use the API key provided in constants.py to make a request to the AESO API

2. Pull down the following data:
   1. Actual Forecast Report
   2. Pool Price Report
   
3. Once that is finished, use the environment Canada API (https://api.weather.gc.ca/) to fetch the weather data for Calgary
   1. This should include daily temperatures, percipitation information, wind speed (wind generation), and sunlight hours (solar) and forecasting data
   
4. Also, use pandas to import more granular xls data from excel files to be provided by Neal in the folder data > raw

5. If we have city granular energy use for Calgary, then we can use said usage and weather for the city. 
   1. Public holidays (https://date.nager.at/Api) - binary or classification - do different holidays have more impact?
   2. natural gas prices (https://www.eia.gov/opendata/) (https://github.com/gavram/Henry-Hub-Gas-Prices/blob/master/daily.py)
   3. big events (maybe??) - like stampede - check if there is an impact first before including it as a feature 
   4. weather (https://api.weather.gc.ca/) - wind and solar rely on the weather - amount of sunshine/amount of wind impact generation - have to look at locale of generation though
   5. length of daylight (sunrise/sunset) - this is intrinsic with date
   6. Historical Demand (AESO)
   
