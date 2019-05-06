import numpy as np
import pandas as pd

import statsmodels
from statsmodels.tsa.stattools import coint
# just set the seed for the random number generator
np.random.seed(107)

import matplotlib.pyplot as plt
import pandas_datareader.data as web
import seaborn

def find_cointegrated_pairs(data):
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            result = coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.02:
                pairs.append((keys[i], keys[j]))
    return score_matrix, pvalue_matrix, pairs




instrumentIds = ['SPY','AAPL','ADBE','SYMC','EBAY','MSFT',
               'QCOM', 'HPQ','JNPR','AMD','IBM']

df = web.DataReader(instrumentIds, 'yahoo', '2007/12/01', '2017/12/01')

data = df['Adj Close']

scores, pvalues, pairs = find_cointegrated_pairs(data)

m = [0,0.2,0.4,0.6,0.8,1]
seaborn.heatmap(pvalues, xticklabels=instrumentIds, 
                yticklabels=instrumentIds, cmap='RdYlGn_r', 
                mask = (pvalues >= 0.98))
plt.show()

print (pairs)

