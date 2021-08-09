import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

user_stock = input("Enter stock ticker symbol: ")
print(user_stock)

s_year = 2017
s_month = 1
s_day = 1

start = dt.datetime(s_year, s_month, s_day)

now = dt.datetime.now()

df = pdr.get_data_yahoo(user_stock, start, now)

# ma = 50  # moving average

# smaString = "S-Moving Average" + str(ma)
# df[smaString] = df.iloc[:, 4].rolling(window=ma).mean()

# Creating exponential moving averages

emasUsed = [3, 5, 8, 10, 12, 15, 30, 35, 40, 45, 50, 60]

for i in emasUsed:
    ema = i
    # Makes a column corresponding to the exponential moving average value
    # ewm() makes it exponential and we round it to 2 decimal places
    # df.iloc[:, 4] goes through the df of the stock and its info in a specific column and uses that data to calc
    # the exponential moving average
    df["Ema_" + str(ema)] = round(df.iloc[:, 4].ewm(span=ema, adjust=False).mean(), 2)
print(df.tail())  # tail() lets us see the last couple of columns of the data frame

# Now we will iterate through each date and see if our entry setup has been satisfied

p_os = 0  # determines if we are entering a position
num = 0  # keeps track of the row that we are on
percent_change = []  # where we add the results of our trade

for i in df.index:
    # The minimum of the short term EMAs
    cmin = min(df["Ema_3"][i], df["Ema_5"][i], df["Ema_8"][i], df["Ema_10"][i], df["Ema_12"][i], df["Ema_15"][i])
    # The maximum of the long term EMAs
    cmax = min(df["Ema_30"][i], df["Ema_35"][i], df["Ema_40"][i], df["Ema_45"][i], df["Ema_50"][i], df["Ema_60"][i])

    # closing value at the point cmin and cmax
    close = df["Adj Close"][i]

    if cmin > cmax:  # If we are in a red, white, blue pattern
        print("Red White Blue")
        # Simulating entering/exiting trade
        if p_os == 0:
            # We are setting our buy price, setting our position, and buying at the price at str(bp)
            bp = close
            p_os = 1
            print("Buying now at " + str(bp))
    elif cmin < cmax:
        print("Blue White Red")
        if p_os == 1:  # If we had a position, we will exit
            p_os = 0
            sp = close
            print("Selling now at " + str(sp))
            pc = (sp / bp - 1) * 100  # calculating how much we bought and sold it for in terms of percentage change
            percent_change.append(pc)

    # If we are at the end date/row then we will exit like if cmin < cmax
    if (num == df["Adj Close"].count() - 1 and p_os == 1):
        p_os = 0
        sp = close
        print("Selling now at " + str(sp))
        pc = (sp / bp - 1) * 100  # calculating how much we bought and sold it for in terms of percentage change
        percent_change.append(pc)

    num += 1

print(percent_change)

# This portion of code analyzes the percent_change list

gains = 0  # Gains in terms of percentage
num_gains = 0
losses = 0  # Losses in terms of percentage
num_losses = 0
total_Return = 1

for i in percent_change:
    if i > 0:
        gains += i
        num_gains += 1
    else:
        losses += i
        num_losses += 1
    # This multiplies all the total percentages together to see what would be the gross return if you were going in
    # 100% in each trade
    total_Return = total_Return * ((i / 100) + 1)
    print("Total Return:" + str(total_Return))
# Makes the total_return cleaner and outputs it out as a percentage
total_Return = round((total_Return - 1)*10, 2)

# Calculating our average gain and average loss

if (num_gains > 0):
    avgGain = gains / num_gains
    maxR = str(max(percent_change))  # Finds the trade that yielded the greatest return
else:
    avgGain = 0
    maxR = "No good trade"
if (num_losses > 0):
    avgLoss = losses / num_losses
    maxL = str(min(percent_change))
    ratio = str(-avgGain / avgLoss) # displaying the risk/reward ratio
else:
    avgLoss = 0
    maxL = "No bad trade"
    ratio = "infinite"

# Finding our batting average/ how many times our trade ended in a gain

if num_gains > 0 or num_losses > 0:
    battingAvg = num_gains/(num_gains + num_losses)
else:
    battingAvg = 0

print()
print("Results for " + user_stock + " going back to " + str(df.index[0])+", Sample size: " + str(num_gains+num_losses) +
      " trades")
print("EMAs used: " + str(emasUsed))
print("Batting Avg: " + str(battingAvg))
print("Gain/loss ratio: " + ratio)
print("Average Gain: " + str(avgGain))
print("Average Loss: " + str(avgLoss))
print("Max Return: " + maxR)
print("Max Loss: " + maxL)
print("Total return over "+str(num_gains+num_losses) + " trades: " + str(total_Return)+"%")
# print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )
print()