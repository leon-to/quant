import numpy as np
import pandas as pd
import statsmodels
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import seaborn
import statsmodels.formula.api as sm

#def zscore_2(series):
#    return (series - series.mean()) / np.std(series)
#
#def zscore(x, window):
#    r = x.rolling(window=window)
#    m = r.mean().shift(1)
#    s = r.std(ddof=0).shift(1)
#    z = (x-m)/s
#    return z


instrumentIds = ['ADBE', 'MSFT']

df = web.DataReader(instrumentIds, 'yahoo', '2007/12/01', '2019')

data = df['Adj Close']

S1 = data['ADBE']
S2 = data['MSFT']
score, pvalue, _ = coint(S1, S2)
print(pvalue)
ratios = S1 / S2

plt.figure()
ratios.plot()
plt.axhline(ratios.mean())
plt.legend([' Ratio'])
plt.show()

## z score
#plt.figure()
#zscore(ratios).plot()
#plt.axhline(zscore(ratios).mean())
#plt.axhline(1.0, color='red')
#plt.axhline(-1.0, color='green')
#plt.show()

# scatter
plt.figure()


ols_result = sm.ols('ADBE ~ MSFT', data=data).fit()
b = ols_result.params['MSFT']

# market portfolio
#data = data['2012':'2017']
#mp = data['ADBE'] - 2.231692*data['MSFT']
#
## z score
#plt.figure()
#z_score = (mp-mp.mean())/mp.std()
#rz_score = zscore(mp, 15)
##rz_score = zscore_2(z_score)
#rz_score = rz_score.dropna()
##z_score.plot()
#rz_score.plot()
#
#long = rz_score[rz_score<-1.5]
#long_close = rz_score[rz_score>=-0.5]
#short = rz_score[rz_score>1.5]
#short_close = rz_score[rz_score<=0.5]
#
#long.plot(color='g', linestyle='None', marker='^')
#long_close.plot(color='r', linestyle='None', marker='^')
#short.plot(color='y', linestyle='None', marker='o')
#short_close.plot(color='b', linestyle='None', marker='o')
#
## trade
#z_entry = 1.5
#z_exit = 0.5
#money = 100000
#q = 1
#b = 2.231692
#invested = False
#position = None
#for i in rz_score.index:
#    if invested == False:
#        if rz_score[i] < -z_entry:
#            # long entry 
#            # purchase 1 ADBE & short 2.2 MSFT
#            money = q*(-s1[i] + b*s2[i])
#            invested = True
#            position = 'LONG'
#            print('LONG: ', money)
#        elif rz_score[i] > z_entry:
#            # short entry
#            money = q*(s1[i] - b*s2[i])
#            invested = True
#            position = 'SHORT'
#            print('SHORT: ', money)
#    elif invested == True:
#        if position == 'LONG' and rz_score[i] >= -z_exit:
#            # long close
#            money = q*(s1[i] - b*s2[i])
#            invested = False
#            position = None
#            print('LONG CLOSE: ', money)
#        elif position == 'SHORT' and rz_score[i] <= z_exit:
#            # short close
#            money = q*(-s1[i] + b*s2[i])
#            invested = False
#            position = None
#            print('SHORT CLOSE: ', money)


data = data['2018']

s1 = data['ADBE']
s2 = data['MSFT']

plt.figure()
plt.scatter(s1, s2)


ratios = s1/s2
w1 = 6
w2 = 60
ma1 = ratios.rolling(w1).mean()
ma2 = ratios.rolling(w2).mean()
std = ratios.rolling(w2).std()
zscore = (ma1-ma2)/std

plt.figure()
zscore.plot()

money = 0
countS1 = 0
countS2 = 0
q = 100
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