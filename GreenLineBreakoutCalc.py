# Green lines signify a significant level of resistance. Usually occurs once a stock hits a ATH and then rests and
# consolidates for a couple of months
import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr

yf.pdr_override()

start_date = dt.datetime(1980, 12, 1)
now = dt.datetime.now()
stock = input("Enter the stock symbol (Type quit to exit): ")

while stock != "quit":
    df = pdr.get_data_yahoo(stock, start_date, now)  # This gets daily data from yahoo finance, but we need monthly data

    df.drop(df[df["Volume"] < 1000].index, inplace = True)
    df_mon = df.groupby(pd.Grouper(freq="M"))["High"].max()  # The "M" stands for month

    # now we want to look a those monthly high datas and compare them
    glDate = 0  # Green line date. The date of the most recent green line value
    lastGLV = 0  # The most recent green line value
    currentDate = ""  # The current date of the glv that the program is keeping track of
    currentGLV = 0  # The current glv that the program is keeping track of
    counter = 0  # Checks if 3 months have passed

    for index, value in df_mon.items():
        # Check all time high condition
        if value > currentGLV:
            currentGLV = value
            currentDate = index
            counter = 0
        if value < currentGLV:
            counter = counter + 1
            if counter == 3 and ((index.month != now.month) or (index.year != now.year)):
                if currentGLV != lastGLV:
                    print("Current GLV:" + str(currentGLV))
                glDate = currentDate
                lastGLV = currentGLV
                counter = 0
    if lastGLV == 0:  # There are no green lines
        message = stock + " has not formed a green line yet"
    else:
        message = ("Last Green Line: " + str(lastGLV) + " on " + str(glDate))

    print(message)
    stock = input("Enter the stock symbol (Type quit to exit): ")
