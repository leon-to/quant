#from __future__ import print_function
from datetime import datetime
from pandas_datareader import data, wb
import statsmodels.tsa.stattools as ts
import numpy as np
from hurst import hurst

amzn = data.DataReader("AMZN", "yahoo", datetime(2000,1,1),datetime(2015,1,1))
ans = ts.adfuller(amzn['Adj Close'], 1)

#create Geometric Brownian Motion, mean-reverting, and trending series
gbm = np.log(np.cumsum(np.random.randn(100000)) + 1000)
mr = np.log(np.random.randn(100000)+1000)
tr = np.log(np.cumsum(np.random.randn(100000)+1)+1000)

#print HE
he_gbm = hurst(gbm)
he_mr = hurst(mr)
he_tr = hurst(tr)
he_amzn = hurst(amzn['Adj Close'])