# Making a stock screener based on the Mark Minervini's stock criteria
# This program teaches: how to create dialog pop-up boxes to select files to manipulate
# This program will run through each ticker symbol in the excel file and check Mark Minervini's 8 conditions on if a
# stock is ready to go on a run
import datetime as dt
import os.path
import pandas as pd
from pandas import ExcelWriter
from pandas_datareader import data as pdr
import yfinance as yf
from tkinter import Tk  # This is what opens the dialog box
from tkinter.filedialog import askopenfilename

yf.pdr_override()
start_date = dt.datetime(2017, 12, 1)
now = dt.datetime.now()

# Finding the file
filePath = r"/Users/aakashkhanal/Downloads/RichardStocks.xlsx"

# Reading the file of stocks
stock_list = pd.read_excel(filePath)
stock_list = stock_list.head()
print(stock_list)

# Create a dataframe  with the following columns. This is where all the stocks that meet the criteria go to
exportList = pd.DataFrame(columns=["Stock", "RS_Rating", "50 Day MA", "150 Day MA", "200 Day MA", "52 Week Low",
                                   "52 Week High"])

# Index in pandas is how to keep track of rows, keep track of columns by using their name
# This for loop looks through the stocks in the excel sheet from the column "Symbol" and iterates through each index/
# row
# i starts at 1
for i in stock_list.index:
    stock = str(stock_list["Symbol"][i])
    RS_Rating = stock_list["RS Rating"][i]

    try:
        df = pdr.get_data_yahoo(stock, start_date, now)

        # Creating and calculating the simple moving average for the "stock" and creating a column in the df for it
        sma_list = [50, 150, 200]
        for s in sma_list:
            sma = s
            df["SMA_" + str(sma)] = round(df.iloc[:, 4].rolling(window=sma).mean(), 2)

        # Accesses the most recent Adjusted Close in the yahoof database
        current_close = df["Adj Close"][-1]
        moving_average_50 = df["SMA_50"][-1]
        moving_average_150 = df["SMA_150"][-1]
        moving_average_200 = df["SMA_200"][-1]

        # Getting the low and high of 52 weeks
        low_of_52W = min(df["Adj Close"][-260:])
        high_of_52W = max(df["Adj Close"][-260:])

        # This checks condition 3
        try:
            mva_200_20_past = df["SMA_200"][-20]
        except Exception:
            mva_200_20_past = 0

        print("Checking " + stock + "...")  # Checking if yahoo finance has data on this stock

        # Pre- assiginging conditions false
        cond_1, cond_2, cond_3, cond_4, cond_5, cond_6, cond_7, cond_8 = False, False, False, False, False, False, False, False
        # Condition 1: Current Price > 150 SMA and > 200 SMA
        if (current_close > moving_average_150) and (current_close > moving_average_200):
            cond_1 = True
        # Condition 2: 150 SMA  > 200 SMA
        if moving_average_150 > moving_average_200:
            cond_2 = True
        # Condition 3: 200 SMA trending up for at least 1 month (ideally 4-5 months)
        if moving_average_200 > mva_200_20_past:
            cond_3 = True
        # Condition 4: 50 SMA> 150 SMA and 50 SMA> 200 SMA
        if (moving_average_50 > moving_average_150) and (moving_average_50 > moving_average_200):
            cond_4 = True
        # Condition 5: Current Price > 50 SMA
        if current_close > moving_average_50:
            cond_5 = True
        # Condition 6: Current Price is at least 30% above 52 week low (Many of the best are up 100-300% before
        # coming out of consolidation)
        if current_close > (1.3 * low_of_52W):
            cond_6 = True
        # Condition 7: Current Price is within 25% of 52 week high
        if current_close >= (.75 * low_of_52W):
            cond_7 = True
        # Condition 8: IBD RS rating >70 and the higher the better
        if RS_Rating > 70:
            cond_8 = True

        if cond_1 and cond_2 and cond_3 and cond_4 and cond_5 and cond_6 and cond_7 and cond_8 == True:
            exportList = exportList.append({'Stock': stock, "RS_Rating": RS_Rating, "50 Day MA": moving_average_50,
                                            "150 Day MA": moving_average_150, "200 Day MA": moving_average_200,
                                            "52 Week Low": low_of_52W,
                                            "52 Week High": high_of_52W}, ignore_index=True)
    except Exception:
        print("No data on " + stock)

print(exportList)

newFile = os.path.dirname(filePath) + "/ScreenOutput.xlsx"

# Writing to excel file
writer = ExcelWriter(newFile)
exportList.to_excel(writer, "Sheet 1")
writer.save()
