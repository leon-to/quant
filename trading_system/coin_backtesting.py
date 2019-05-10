from trader2.data import DataHandler
from trader2.analyzer import Analyzer
from trader2.backtest import Backtest
import pandas_datareader.data as web
import pandas as pd

dh = DataHandler()
az = Analyzer(dh)
bt = Backtest(dh)

#pairs = [['ADBE', 'MSFT'], [['EWA', 'EWC']]]
#dh.scrap_pddr_data(pairs[0], 'yahoo', '2018', '2019')
#az.coint()
#bt.run()

df = {}
pairs = ['AREX', 'WLL']

for s in pairs:
    df[s] = pd.read_csv('./data/%s.csv' % s, parse_dates=True)
    
close = pd.DataFrame(index=df[pairs[0]].index)
close['Datetime'] = df[pairs[0]]['Datetime']
close[pairs[0]] = df[pairs[0]]['Adj Close']
close[pairs[1]] = df[pairs[1]]['Adj Close']


for i in range(len(close)):
    print (close.index(i))