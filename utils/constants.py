import os

AESO_API_KEY= os.getenv('AESO_API_KEY')
BASE_URL='https://api.aeso.ca/report'
CURRENT_SUPPLY_DEMAND_URL='v1/csd/summary/current'
INTERNAL_LOAD_URL='v1/load/albertaInternalLoad'
POOL_PRICE_REPORT='v1.1/price/poolPrice'
CALGARY_API_URL='https://api.weather.gc.ca/'
PUBLIC_HOLIDAY_URL='https://date.nager.at/api/v3/PublicHolidays'
EIA_BASE_URL='https://api.eia.gov'
EIA_API_KEY= os.getenv('EIA_API_KEY')
EIA_NATURAL_GAS_URL='v2/natural-gas/pri/fut/data/'
START_YEAR = 2003
END_YEAR = 2023
