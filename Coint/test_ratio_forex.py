import numpy as np
import pandas as pd
import statsmodels
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import seaborn
import statsmodels.formula.api as sm
from datetime import timedelta

data = pd.read_csv('EURUSD_GBPUSD.csv', index_col=0, parse_dates=True)
data = data['2018-1-1']

s1 = data['EURUSD']
s2 = data['GBPUSD']

score, pvalue, _ = coint(s1, s2)
print(pvalue)
ratios = s1 / s2

plt.figure()
plt.scatter(s1, s2)


#ratios
#ratios = s1/s2

ratios = pd.DataFrame(index=data.index, columns=['b'])
lookback = 20
for t in data.index:
    if t < data.index[0] + timedelta(minutes=lookback):
        continue
    ols_result = sm.ols('EURUSD ~ GBPUSD', data=data[t-timedelta(days=lookback):t]).fit()
    ratios.loc[t] = ols_result.params['GBPUSD']
    print(ols_result.params['GBPUSD'])



#fix bug: TODO find better solution
ratios = ratios['b']

spread = s1 - ratios*s2
zscore = (spread-spread.rolling(lookback).mean())/spread.rolling(lookback).std()

#w1 = 6
#w2 = 60
#ma1 = ratios.rolling(w1).mean()
#ma2 = ratios.rolling(w2).mean()
#std = ratios.rolling(w2).std()
#zscore = (ma1-ma2)/std

plt.figure()
zscore.plot()

money = 0
countS1 = 0
countS2 = 0
q = 1000
invested = False

for i in range(len(ratios)):
    date = zscore.index[i]
    # Sell short if the z-score is > 1
    if invested == False:
        if zscore[i] > 1:
            money += q*(s1[i] - s2[i] * ratios[i])
            countS1 -= 1
            countS2 += ratios[i]
            print('%s Selling Ratio %s %s %s %s'%(date, money, ratios[i], countS1,countS2))
            invested = True
        # Buy long if the z-score is < 1
        elif zscore[i] < -1:
            money -= q*(s1[i] - s2[i] * ratios[i])
            countS1 += 1
            countS2 -= ratios[i]
            print('Buying Ratio %s %s %s %s'%(money,ratios[i], countS1,countS2))
            invested = True
    # Clear positions if the z-score between -.5 and .5
    elif invested == True and abs(zscore[i]) < 0.75:
        money += q*(s1[i] * countS1 + s2[i] * countS2)
        countS1 = 0
        countS2 = 0
        print('Exit pos %s %s %s %s'%(money,ratios[i], countS1,countS2))
        invested = False