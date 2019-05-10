import numpy as np
import pandas as pd

import statsmodels
from statsmodels.tsa.stattools import coint, adfuller
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import seaborn



pair_list = [
    ['EWA', 'EWC'], 
    ['ADBE', 'MSFT'], 
    ['SLVP', 'SLV'],
    ['RTH', 'XLP']
]
pair = pair_list[3]

df = web.DataReader(pair, 'yahoo', '2009', '2019')
df = df['Adj Close']
df.dropna(inplace=True)
#df = df['2011':'2012']

cadf, p, _ = coint(df[pair[0]], df[pair[1]])
cadf2, p2, _ = coint(df[pair[1]], df[pair[0]])

plt.scatter(df[pair[0]], df[pair[1]])
df.plot()

#
#plt.figure()
#df['YOLO'].plot()
