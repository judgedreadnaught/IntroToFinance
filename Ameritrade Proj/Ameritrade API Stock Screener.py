# Goes and finds companies that match a certain criteria, ex: p/e ratio of less than 30
import pandas_datareader as pdr
import pandas as pd
import datetime as dt
from yahoo_fin import stock_info as si

tickers = si.tickers_sp500()  # tickers in the sp500
start = dt.datetime.now() - dt.timedelta(days=365)  # 365 days from now, specifying the time frame we are looking at
end = dt.datetime.now()

# Loading data frame of sp500, info of sp500, and then compare it to the individual stocks in sp500,
#  we are trying to see which stocks in the sp500 have beated the sp500

sp500_df = pdr.DataReader('^GSPC', 'yahoo', start, end)
#  Calculating percentage change
sp500_df['Per Change'] = sp500_df['Adj Close'].pct_change()  # Creating a new column called Per Change
#  Calculating returns of sp500, cumprod()[-1] gets the cumulative product of the entire column up to the last row
sp500_return = (sp500_df['Per Change'] + 1).cumprod()[-1]


# Now we will repeat for every single stock in the sp500 and then compare the returns to the sp500

# Creating our data frame that will store the below info about each stock in the sp500
return_list = []
final_df = pd.DataFrame(columns=["Ticker", "Latest Price", "Score", "PE_Ratio", "PEG_Ratio", "SMA_150",
                        "SMA_200", "52_Week_Low", "52_Week_High"])
# Score is how the stock compares to the sp500 returns
for ticker in tickers:
    df = pdr.DataReader(ticker, "yahoo", start, end)
    #df.to_csv(f'stock_data/{ticker}.csv')  # formatting

    df['Per Change'] = df['Adj Close'].pct_change()
    stock_return = (df['Per Change'] + 1).cumprod()[-1]

    returns_compared = round((stock_return / sp500_return), 2)
    return_list.append(returns_compared)

# Finding the best performers of all the tickers
best_performers = pd.DataFrame(list(zip(tickers, return_list)), columns=["Ticker", "Returns Compared"])
# Rank method ranks the best performers, pct means percentage
best_performers['Score'] = best_performers['Returns Compared'].rank(pct=True) * 100
# Now we only leave the best performers and cut out the rest, quantile(80) means you are picking the top 20%
best_performers = best_performers[best_performers["Score"] >= best_performers['Score'].quantile(70)]

