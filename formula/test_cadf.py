import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import pprint
import statsmodels.tsa.stattools as ts
import cadf
import statsmodels.formula.api as sm

start = dt.datetime(2012,1,1)
end = dt.datetime(2013,1,1)

arex = web.DataReader('AREX', 'yahoo', start, end)
wll = web.DataReader('WLL', 'yahoo', start, end)

df = pd.DataFrame(index=arex.index)
df['AREX'] = arex['Adj Close']
df['WLL'] = wll['Adj Close']

cadf.plot_price_series (df, 'AREX', 'WLL')
cadf.plot_scatter_series (df, 'AREX', 'WLL')

#calculate optimal hedge ratio beta
res = sm.ols ('WLL ~ AREX', data=df).fit()
params = res.params
beta_hr = res.params['AREX']


#calculate residuals of linear combination
df['res'] = df['WLL'] - beta_hr*df['AREX']

#plot residuals
cadf.plot_residuals(df)

#calculate cadf
cadf_result = ts.adfuller(df['res'])
