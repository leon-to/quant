import datetime
import numpy as np
import pandas as pd
import pandas_datareader.data as data

# =============================================================================
# Calculate the annualised Sharpe ratio of a return stream based on a number
# of trading periods, N (default 252) which then assumes a stream of daily 
# returns.
# =============================================================================
def annualised_sharpe (returns, N=252):
    return np.sqrt(N) * returns.mean() / returns.std()

# =============================================================================
# calculate annualised sharpe ratio based on daily returns of an equity ticker
# symbol listed in  google finance
# =============================================================================
def equity_sharpe (ticker):
    start = datetime.datetime(2000,1,1)
    end = datetime.datetime(2013,1,1)
    
    #obtain equities data for time period and add to pandas dataframe
    pdf = data.DataReader(ticker, 'yahoo', start, end)
    
    #use percentage change method to easily calculate daily returns
    pdf['daily_ret'] = pdf['Close'].pct_change()
    
    #assume an average annual risk-free rate over the period of 5%
    pdf['excess_daily_ret'] = pdf['daily_ret'] - 0.05/252
    
    return annualised_sharpe (pdf['excess_daily_ret']), pdf

# =============================================================================
# calculate the annualised Sharpe ratio of a market neutroal long/short
# strategy involving the long of 'ticker' with a corresponding short of the
# 'benchmark'
# =============================================================================
def market_neutral_sharpe(ticker,benchmark):
    start = datetime.datetime(2000,1,1)
    end = datetime.datetime(2013,1,1)
    
    #get data
    tick = data.DataReader(ticker,'yahoo', start, end)
    bench = data.DataReader(benchmark, 'yahoo', start, end)
    
    #compute percentage returns
    tick['daily_ret'] = tick['Close'].pct_change()
    bench['daily_ret'] = bench['Close'].pct_change()
    
    #create new dataframe to store strategy info
    #net returns are (long-short)/2 since there is twice trading capital
    strat = pd.DataFrame(index=tick.index)
    strat['net_ret'] = (tick['daily_ret']-bench['daily_ret'])/2.0
    
    #return annualised Sharpe ratio for this strategy
    return annualised_sharpe(strat['net_ret'])