# python_candlestick_chart.py
import sys
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates

def stock():
    stock = "ptt.bk"
    start = "2021-01-12"
    end = "2021-03-12"

    try:
        df = pdr.get_data_yahoo(stock, start=start, end=end)
        print(df.to_csv())
    except:
        print("Error:", sys.exc_info()[0])
        print("Description:", sys.exc_info()[1])

    with open('stock.csv', 'w', newline='', encoding='utf-8') as f:
        f.write(df.to_csv())
    plot_candal()
    #plot_stock2()
    #plot_stock()

def plot_candal():
    plt.style.use('ggplot')

    # Extracting Data for plotting
    data = pd.read_csv('stock.csv')
    ohlc = data.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
    ohlc['Date'] = pd.to_datetime(ohlc['Date'])
    ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float)

    # Creating Subplots
    fig, ax = plt.subplots()

    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
    # Setting labels & titles
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    fig.suptitle('Stock')


    # Formatting Date
    date_format = mpl_dates.DateFormatter('%d-%m-%Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    fig.tight_layout()

    # python_candlestick_chart.py

    ohlc['SMA5'] = ohlc['Close'].rolling(5).mean()
    ax.plot(ohlc['Date'], ohlc['SMA5'], color='green', label='SMA5')

    fig.suptitle('Daily Candlestick Chart of NIFTY50 with SMA5')

    plt.legend()

    plt.show()


stock()