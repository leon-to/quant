import fix_yahoo_finance as yf
import pandas as pd

symbols = ['SPY', 'AAPL', 'AREX', 'WLL']

data = yf.download(symbols, 
                   start="2019-05-01", end="2019-05-07",
                   interval = "1m")
data.dropna(inplace=True)

df = {}
for symbol in symbols:
    df[symbol] = data.xs(symbol, 1, 1)
    df[symbol] = df[symbol][['Open', 'Low', 
                    'High', 'Close', 'Volume', 'Adj Close']]
    df[symbol].to_csv('./data/%s.csv' % symbol)