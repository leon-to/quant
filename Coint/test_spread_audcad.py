import numpy as np
import pandas as pd
import statsmodels
from statsmodels.tsa.stattools import coint, adfuller
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import seaborn
import statsmodels.formula.api as sm
from datetime import datetime, timedelta


aud = pd.read_csv('AUDUSD_D1_Ask.csv', index_col=0, parse_dates=True)
cad = pd.read_csv('USDCAD_D1_Ask.csv', index_col=0, parse_dates=True)

df = pd.DataFrame(index=aud.index)
df['USDAUD'] = 1/aud['Close']
df['USDCAD'] = cad['Close']
df.dropna(inplace=True)

#df = df['2017':'2019']

ols = sm.ols('USDAUD ~ USDCAD', data=df).fit()

cadf, pvalue, _ = coint(df['USDAUD'], df['USDCAD'])
cadf2, pvalue2, _ = coint(df['USDCAD'], df['USDAUD'])

ols.resid.plot()
df.plot()