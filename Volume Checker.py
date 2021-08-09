import math
import yfinance as yf
import pandas as pd
import datetime as dt
from pandas_datareader import data as pdr
import yahoo_fin
import yahoo_fin.stock_info as si


# Function that calculates if a particular volume deviates too much from the standard deviation of previous day(s)
# average volume
def standard_dev_calc(volumes, current_vol, deviation=10.0):  # Volumes is the list of volumes for a particular stock,
    # deviation is how much you wanna check it deviates from the mean. Default value for deviation is 10
    mean = float(0.0)
    standard_dev = float(0.0)

    for volume in volumes:
        mean += float(volume)
    mean = float(mean / len(volumes))  # Getting the mean of the volumes

    for num in volumes:
        standard_dev += math.pow(num - mean, 2)
    standard_dev = math.sqrt(standard_dev / len(volumes))
    print("Mean is: " + str(round(mean, 3)))
    print("Standard deviation is: " + str(round(standard_dev, 3)))

    deviated = (deviation * standard_dev) + mean
    print("Volume must deviate " + str(round(deviated,3)) + " from mean to be notable.")
    new_vol = int(current_vol) # current_vol comes in as a series
    if deviated <= new_vol:
        print("Buy\n")
    else:
        print("Nothing unusual\n")


yf.pdr_override()

print("Unusual Stock Volume Checker for Stocks in Dow Jones!\n")
# Get a list of tickers from Dow Jones
dow_list = si.tickers_dow()

# Assign tickers their historical data
dow_historical = {}

"""Ask user if they want a specific ticker or all stocks, and ask how far back they want to go in checking the volume"""
user_in = input("Would you like to run this on a particular stock or for all stocks in the Dow Jones?"
                " (Type ALL or Ticker_Symbol): ").upper()

"""Extract numbers and days/weeks from input, while doing error handling"""
x = True
while x:
    user_date = input("How far back would you like to check the volume?(1-5d, 1w, or 2w): ")
    user_date = user_date.upper()
    res = [int(i) for i in user_date if i.isdigit()]  # This is a list
    num_days = res[0]  # How far they want to go, 1-5 days or 1-5 weeks
    type_day = user_date[-1]  # Either this is D or W, day or week
    # print(num_days)
    # print(type_day)
    if (1 <= num_days <= 5) and (type_day == "D" or type_day == "W"):
        x = False
    else:
        print("Please put in a valid input")

"""Adjust start_date for si.get_data """
if type_day == "D":
    start_date = dt.date.today() - dt.timedelta(days=num_days)
else:
    start_date = dt.date.today() - dt.timedelta(weeks=num_days)

""" Get ticker information for every ticker in Dow Jones from a certain date"""
for ticker in dow_list:
    dow_historical[ticker] = si.get_data(ticker, start_date)  # (ticker, start_date)

""" Check if user_in is a valid ticker input"""
counter = 0
x = True;
while x:
    if user_in == "ALL" or user_in == dow_list[counter]:
        x = False
    else:
        counter += 1
        if counter > 29:
            print("Stock ticker is invalid, not found in Dow Jones Index")
            counter = 0
            user_in = input("Would you like to run this on a particular stock or for all stocks in the Dow Jones?"
                            " (Type ALL or Ticker_Symbol): ").upper()

""" Now we have valid user input and date set """
# Display the data frame for every single stock from start_date
if user_in == "ALL":
    dev_in = float(input("What would you like your deviation to be?: " ))
    for ticker in dow_list:
        print(dow_historical[ticker])
    for ticker in dow_list:
        print("TICKER:" + str(ticker).upper())
        current_vol = si.get_data(ticker, dt.date.today()).get("volume")  # This gets the current volume of each ticker
        # in dow_list. Get it by reloading the table dow_list with data of the current day only , turning it into
        # dictionary dow_historical, and then only getting the volume column. You have to do si._get_data because
        # we need volume from a specific date only, not a list of volumes that has already been determined by our prev
        # start_date variable.
        int_vol = int(current_vol)
        print("Current Volume: " + str(current_vol))
        volumes = dow_historical[ticker].get("volume")
        standard_dev_calc(volumes, current_vol, dev_in)
else:
    dev_in = float(input("What would you like your deviation to be?: " ))
    print("TICKER:" + str(user_in))
    current_vol = si.get_data(user_in, dt.date.today()).get("volume")
    int_vol = int(current_vol)
    print("Current Volume: " + str(current_vol))
    volumes = dow_historical[user_in].get("volume")
    standard_dev_calc(volumes, current_vol, dev_in)

# print(dow_historical["AAPL"].get("volume"))
# info = dow_historical["AAPL"].get("volume")
# print(info)
# Conditional based on user_in
# if (user_in.capitalize() == "ALL"):
