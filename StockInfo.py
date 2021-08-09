import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()  # Yahoo finance decommissioned their historical data API, this returns the web scraped data from
# Yahoo finance and returns
# def get_start_d(month=1, day=1, year=2000):


# The stock the user wants to look up
user_stock = input("Enter stock ticker symbol: ")
print(user_stock)

# What time period they want the stock data to be from. Default is 1/1/2000. There are some edge cases, such as making
# sure the month and day are valid, that need to be fixed.
month = -1
day = -1
year = -1
while True:
    try:
        month = int(input("Month: "))
        day = int(input("Day: "))
        year = int(input("Year (2000 or after): "))
        if month > 0 and day > 0 and (2000 <= year <= dt.date.today().year):  # this dt.today gets us the current year
            break
        else:
            raise ValueError
    except ValueError:
        print("Please enter a valid number for the Month, Day, or Year")
        continue

# The above input gives us the start date for our stock ticker
start_date = dt.datetime(year, month, day)
current_date = dt.datetime.now()  # We get the stock data up til now

# Storing all the stock data in a dataframe
df = pdr.get_data_yahoo(user_stock, start_date, current_date)
#print(df)

# Making moving average using Adj close prices. Open is the 0th column, Adj close is the 4th column
moving_avg = 50  # how many days our moving average is going to use
s_moving_avg = "Sma_" + str(moving_avg)

# df[s_moving_avg] creates a column titled S_moving_avg. df.iloc[:, 4] utilizes the 4th column of df to do the average.
# rolling(window=...).mean() calculates the rolling moving average with a window size of our moving average (50 days
# for now).
df[s_moving_avg] = df.iloc[:, 4].rolling(window=moving_avg).mean()
# print(df)
# The first 50 rows don't have an s_moving_avg because there is not enough days to take the average of. This code
# cuts out the first 50 rows.
df = df.iloc[moving_avg:]
print(df)

# This for loop gives us each of the dates in the table only, because the dates are the indices of the data frame
# iloc() lets us retrieve rows from our data frame. [:] gives us the entire row.[4] gives us column 4

# counters to keep track of how many times it closes higher or lower
counter_h = 0
counter_l = 0
for i in df.index:
    # print(df.iloc[:, 4][i])  # This prints the adjusted close for each date

    # print(df["Adj Close"][i]) # This also prints the adjusted close for each date, utilizing the column name

    # compare the adjusted close with the moving average
    if df["Adj Close"][i] > df[s_moving_avg][i]:
        print("The close is higher")
        counter_h += 1
    else:
        print("The close is lower")
        counter_l += 1

print(counter_h)
print(counter_l)