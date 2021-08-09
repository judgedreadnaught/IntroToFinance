import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

yf.pdr_override()  # yf workaround
start = dt.datetime(2017, 1, 1)
now = dt.datetime.now()

stock = input("Enter Stock Symbol: ")
while stock.upper() != "QUIT":

    df = pdr.get_data_yahoo(stock, start, now) # Gets stock price data

    # Plotting the stocks data normally, but we're only plotting the high data of the stock before it got knocked down

    df["High"].plot(Label="high")

    pivots = []  # stores the pivot values we calc
    dates = []  # stores the dates at which the pivot points occur
    counter = 0  # counts how many days occurred before a max happened. Goes by period of 5 days. Finds local max in
    # a 5 day period to the left and to the right
    last_pivot = 0  # stores the last pivot value

    # Each day we are going to add a new value and get rid of the last
    range_days = [0, 0, 0, 0, 0, 0, 0, 0, 0] # keeping track of the 5 day period
    dateRange = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in df.index:
        currentMax = max(range_days, default=0)
        value = round(df["High"][i], 2)

        range_days = range_days[1:9]
        range_days.append(value)
        dateRange = dateRange[1:9]
        dateRange.append(i)

        if currentMax == max(range_days, default=0):
            counter += 1
        else:
            counter = 0
        if counter == 5:
            last_pivot = currentMax
            dateloc = range_days.index(last_pivot)
            last_date = dateRange[dateloc]
            pivots.append(last_pivot)
            dates.append(last_date)
    print()

    time_delta = dt.timedelta(days=30)

    for index in range(len(pivots)):
        print(str(pivots[index]) + ": " + str(dates[index]))

        plt.plot_date([dates[index], dates[index] + time_delta], [pivots[index], pivots[index]],
                      linestyle="-", linewidth=2, marker=",")
    plt.show()

    stock = input("Enter the stock symbol: ")