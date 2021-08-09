import yfinance as yf
import streamlit as st
from datetime import date
from plotly import graph_objs as go

# Getting dates
start = "2015-01-01"
today = date.today().strftime("%Y-%m-%d")

st.title("Stock WebApp")

# Stocks whose graphs we can see
stocks = ("GOOG", "AAPL", "GME", "MSFT")
selected_stocks = st.selectbox("Select datset for prediction", stocks)  # Dropdown menu

n_years = st.slider("Years", 1, 4)  # The start value is 1 and end value is 4
period = n_years * 365  # period is in days


# Whenever we interact with these widgets the values in them get updates

@st.cache  # Whenever we download the data, we cache it so we dont have to download it again
def load_data(ticker):  # Loads data from ticker
    data = yf.download(ticker, start, today)  # returns the data in a pandas data frame
    data.reset_index(inplace=True)  # This argument will put the dates in the first column
    return data


# When the datat is done loading this shows up
data_load_state = st.text("Load data...")  # This is a widget
data = load_data(selected_stocks)
data_load_state.text("Loading data...done!")

st.subheader("Raw Data: " + selected_stocks)
st.write(data.tail())  # This can handle any pandas dataframem, we will get the tail of the ticker's data
# This st.write just prints out on the website what is put into the argument


# Now we will plot the data. We will plot the opening prices on each date


def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()
