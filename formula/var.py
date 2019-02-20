import datetime
import numpy as np
import pandas_datareader.data as data
from scipy.stats import norm

# =============================================================================
# variance-covariance calculation of daily value-at-risk using confidence 
# level c, with means of returns mu and standard deviation of returns signma,
# on a portfolio of value P
# =============================================================================
def var_cor_var (P,c, mu, sigma):
    alpha = norm.ppf(1-c, mu, sigma)
    return P - P*(alpha+1)

start = datetime.datetime(2010,1,1)
end = datetime.datetime(2014,1,1)

citi = data.DataReader('C', 'yahoo', start,end)
citi['rets'] = citi['Adj Close'].pct_change()

P = 1e6 # 1mil USD
c = 0.99 # 99% confidence interval
mu = np.mean(citi['rets'])
sigma = np.std(citi['rets'])

# value at risk = $56472.6
var = var_cor_var (P,c,mu,sigma)
