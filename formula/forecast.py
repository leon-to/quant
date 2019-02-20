import datetime
import numpy as np
import pandas as pd
import pandas_datareader.data as data
import sklearn.discriminant_analysis as da
# =============================================================================
# create a pandas dataframe that stores percentage return of adjusted closing
# value of stock from Yahoo, along with a number of lagged returns from prior
# trading days (lags default to 5 days). Trading volume, as well as direction
# from previous day, are also included
# =============================================================================
def create_lagged_series (symbol, start_date, end_date, lags=5):
    # obtain stock info from yahoo
    ts = data.DataReader(
            symbol, 
            'yahoo',
            start_date - datetime.timedelta(days=365),
            end_date)
    
    #create new lag dataframe
    tslag = pd.DataFrame(index=ts.index)
    tslag['Today'] = ts['Adj Close']
    tslag['Volume'] = ts['Volume']
    
    #create a shifted lag series of prior trading period close values
    for i in range(lags):
        tslag['Lag%s' % (i+1)] = ts['Adj Close'].shift(i+1)
        
    #create return dataframe
    tsret = pd.DataFrame(index=tslag.index)
    tsret['Volume'] = tslag['Volume']
    tsret['Today'] = tslag['Today'].pct_change() * 100.0
    
    # if anyvalue of percentage change equal 0, set them to a smaller number
    # (stop issues with QDA model in Scikit-learn)
    for i,x in enumerate(tsret['Today']):
        if(abs(x) < 0.0001):
            tsret['Today'][i] = 0.0001
            
    # create lag percentage return columns
    for i in range(lags):
        tsret['Lag%s' % (i+1)] = tslag['Lag%s' % (i+1)].pct_change() * 100.0
        
    # create direction column indicating up/down days
    tsret['Direction'] = np.sign(tsret['Today'])
    tsret = tsret[tsret.index >= start_date]
    
    return tsret
    
    
    