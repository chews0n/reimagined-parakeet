import os
import requests
import json
import csv
import matplotlib
from matplotlib import pyplot as plt

api_url_daily = "https://api.eia.gov/series/?api_key=" \
                + "76c7b40fb506528c68e66cc40d1a2670&series_id=NG.RNGWHHD.D"

# Obtaining Daily and Monthly Data for Natural Gas Prices, then writing in
# "CSVs\daily.csv" and "CSVs\monthly_from_daily_api.csv",
# using daily API series_id

# Daily Prices
json_data = requests.get(api_url_daily).json()
with open('data/CSVs/daily.csv', 'w', newline="") as csvfile:
    writer_day = csv.writer(csvfile)
    writer_day.writerow(['Date', 'Price'])
    for pair in json_data ['series'][0]['data']:
        date = pair[0]
        date_day = date[4:6] + "/" + date[6:8] + "/" + date[0:4]
        price = pair[1]
        if bool(price):
            writer_day.writerow([date_day, price])

# Monthly Prices as prices for the first day of the month
# for which data is available, from Daily API
with open('data/CSVs/monthly_from_daily_api.csv', 'w', newline="") as csvfile:
    writer_month = csv.writer(csvfile)
    writer_month.writerow(['Month/Year', 'Price'])
    n = len(json_data ['series'][0]['data'])
    for i in range(0,n-1):
        if i > 0 :        
            pair = json_data ['series'][0]['data'][i]
            pair_prev = json_data ['series'][0]['data'][i-1]
            date = pair[0]
            date_prev = pair_prev[0]
            if int(date_prev[4:6])>int(date[4:6]) or \
               int(date[0:4]) > int(date_prev[0:4]):
                date_new = date[4:6] + "/" + date[0:4]
                price = pair[1]
                writer_month.writerow([date_new, price])
        i = i + 1

# Wait for user input
# Displaying Daily chart on screen
print("Data is stored in CSVs/daily.csv and" \
      + "CSVs/monthly_from_daily_api.csv")
key = input("Do you want to print a chart? Press 'y'" \
            + "to print chart or any other key to quit program: " )
if key == 'y':
    # Printing chart
    x = []
    y = []
    with open('CSVs/daily.csv','r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in plots:
            if i > 0:
                x.append(float(row[0][6:11]) + float(row[0][0:2])/12 + float(row[0][3:5])/365)
                y.append(float(row[1]))
            i = i + 1

    plt.figure(figsize=(30, 10))
    plt.plot(x, y, label='Natural Gas Daily Prices')
    plt.xlabel('Month')
    plt.ylabel('Price')
    plt.title('Natural Gas Daily Prices')
    plt.axis([1997, 2020, 0, 20])
    plt.grid(True)
    plt.legend()
    plt.show()