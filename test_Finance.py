from pandas_datareader import data as pdr
import pandas as pd
import sys
import csv
import matplotlib.pyplot as plt

stock = 'BTC-USD'
start = "2021-02-10"
end = "2021-03-10"

try:
    ptt = pdr.get_data_yahoo(stock, start=start, end=end)
    print(ptt['Adj Close'].to_csv())
except:
    print("Error:", sys.exc_info()[0])
    print("Description:", sys.exc_info()[1])

with open('stock.csv', 'w', newline='', encoding='utf-8') as f:
    f.write(ptt['Adj Close'].to_csv())

def plot_stock():
    df = pd.read_csv('stock.csv')
    date = df['Date']
    adj = df['Adj Close']
    plt.plot(date,adj, 'g--')
    plt.xlabel('DATE')
    plt.ylabel('Adj Close')
    plt.title('Stock') 
    plt.show()
    #plt.savefig('C:/software/software2/pic/stock.jpg')
    #graph.setStyleSheet('border-image: url(C:/software/software2/pic/stock.jpg);')

plot_stock()