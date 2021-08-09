# This program attempts to optimize a users portfolio using teh Efficient Frontier
# Portfolio optimization is selecting the best portfolio out of a list of portfolios based on a set of criteria
import pandas as pd
from pandas import DataFrame
from pandas_datareader import data as web
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

# Get the stock symbols in the portfolio after creating a fictional portfolio.
portfolio = ["FB", "AAPL", "NFLX", "GOOG", "AMZN"]

# Assign weights to the stocks. Weights must add up to equal one, because it is a percentage of our portfolio.
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])  # we have a 20% stake in each one of these stocks

# Get the portfolio start date
start_date = dt.datetime(2013, 1, 1)

# Get the stocks ending date (today)
today = dt.datetime.today().strftime('%Y-%m-%d')
#print(today)

# Create a dataframe to stare the adjusted close price of the stocks
df = pd.DataFrame()
for stock in portfolio:
    df[stock] = web.DataReader(stock, data_source="yahoo", start=start_date, end=today)["Adj Close"]  # returns the
    # adjusted close
#print(df)

# Visually showing the stock/portfolio
title = "Portfolio Adj. Close Price History"
# Create and plot the graph
for c in df.columns.values:
    plt.plot(df[c], label=c)

plt.title(title)
plt.xlabel("Date", fontsize=18)
plt.ylabel("Adj. Price USD ($)", fontsize=18)
plt.legend(df.columns.values, loc="upper left")
plt.show()

# Showing the daily simple returns
returns = df.pct_change()

# Showing the annualized covariance matrix
cov_mat_ann = returns.cov() * 252  # 252 is the number of trading days in a year, cov calcualtes the directional
# relationship between two asset prices
#print(cov_mat_ann)

# Calculate the portfolio variance. Formula: weights transposed * covariance matrix * weights
port_var = np.dot(weights.T, np.dot(cov_mat_ann, weights))
#print(port_var)

# Calculate the portfolio volatility aka the standard deviation
port_vol = np.sqrt(port_var)

# Calculate the annual portfolio return
port_simple_ann_return = np.sum(returns.mean() * weights) * 252

# Show the expected annual return, volatility (risk), and the variance
percent_var = str(round(port_var, 2) * 100) + "%"
percent_vol = str(round(port_vol, 2) * 100) + "%"
percent_ret = str(round(port_simple_ann_return, 2) * 100) + "%"


