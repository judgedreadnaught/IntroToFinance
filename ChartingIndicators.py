import yfinance as yf
import datetime as dt
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import datetime as datetime
import numpy as np

yf.pdr_override()

# Moving averages we want to use. We use simple 10,30 and 50 day averages
smasUsed = [10, 30, 50]

start = dt.datetime(2020, 1, 1) - dt.timedelta(days=max(smasUsed))  # This sets the start point for the dataframe, the
# The time delta makes sure we're going far enough in our data to make use of the smas used
now = dt.datetime.now() # Sets end point for dataframe
stock = input("Enter the stock symbol: " ) # Asks for the stock ticker

while stock.upper() != "QUIT":
    prices = pdr.get_data_yahoo(stock, start, now)  # we used prices instead of df as the name

    fig = plt.subplots()  # Create plots
    ax1 = plt.subplots()

    # Calculate the moving averages for all those days
    for x in smasUsed: # This for loop calculates the SMAs for the stated periods and appends to dataframe
        sma = x
        prices['SMA' + str(sma)] = prices.iloc[:, 4].rolling(window=sma).mean()  # calcs the sma and creates col for it


    # Now we will calc the Bollinger Bands. Bollinger Bands are a certain std above and below the sma, and says that
    # the price will be likely between the bands. If the price is above the band, it will most likely come back down
    # and if it is below it will most likely come back up
    bb_period = 20  # this is the moving average we will chose
    st_dev = 2
    # This calcs the sma and creates a col
    prices['SMA' + str(bb_period)] = prices.iloc[:, 4].rolling(window=bb_period).mean()
    prices['STDEV'] = prices.iloc[:, 4].rolling(window=bb_period).std() # calcs the std dev and creates a col
    prices['LowerBand'] = prices["SMA" + str(bb_period)] - (st_dev * prices['STDEV']) # calcs lower bollinger band
    prices['UpperBand'] = prices["SMA" + str(bb_period)] + (st_dev * prices["STDEV"]) # calcs upper bollinger band
    prices['Date'] = mdates.date2num(prices.index)  # creates a date column stored in number format

    # Calculate 10.4.4 stochastic
    Period = 10  # the stoc period
    K = 4  # the K parameter
    D = 4  # the D parameter

    prices["RolHigh"] = prices["High"].rolling(window=Period).max()  # Finds high of the period
    prices["RollLow"] = prices["Low"].rolling(window=Period).min()  # Finds low of the period
    #prices["stoch"] = ((prices["Adj Close"] - prices["RolLow"])/prices["RolHigh"] - prices["RolLow"]) * 100
    #prices["K"] = prices["stoch"].rolling(window=K).mean()  # Finds 10.4 stoch
    #prices["D"] = prices["K"].rolling(window=D).mean()  # Finds 10.4.4 stoch
    #prices["GD"] = prices["High"]  # Creates GD column to store green dots
    ohlc = []

    # Delete extra dates
    prices = prices.iloc[max(smasUsed):]

    greenDotDate=[]  # Stores dates of Green Dots
    greenDot = []  # Stores Values of Green Dots
    lastK = 0  # Will store yesterday's fast stoch
    lastD = 0  # Will store yesterday's slow stoch
    lastLow = 0  # Store yesterday's lower
    lastClose = 0   # Store yesteday's close
    lastLowBB = 0 # stores yesterday's lower bband

    # Plot Moving averages and BBands
    for x in smasUsed:  # This for loop calcs the EMAs for the stated periods and appends to dataframe
        sma = x
        prices["Sma" + str(sma)].plot(Label="close")
    prices["UpperBand"].plot(Label="close", color="lightgray")
    prices["LowerBand"].plot(Label="close", color="lightgray")






