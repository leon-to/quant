import numpy as np
import pandas as pd
import statsmodels
from statsmodels.tsa.stattools import coint, adfuller
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import seaborn
import statsmodels.formula.api as sm
from datetime import datetime, timedelta
import pandas_datareader.data as web

pair_list = [['EWA', 'EWC'], ['ADBE', 'MSFT'], ['CGC', 'cr]]
pair = pair_list[0]

df = web.DataReader(pair, 'yahoo', '2009', '2019')
df = df['Adj Close']
#df = df['2010':'2012']

cadf, p, _ = coint(df[pair[0]], df[pair[1]])
cadf2, p2, _ = coint(df[pair[1]], df[pair[0]])

plt.scatter(df[pair[0]], df[pair[1]])
df.plot()
