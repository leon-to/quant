import numpy as np
from numpy import sqrt, std, subtract, polyfit, log
# =============================================================================
# return Hurst exponent of time series ts
# =============================================================================
def hurst(ts):
    #create range of lag values
    lags = range(2,100)
    #calculate array of variances of lagged differences
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    #use polyfit to estimate Hurst Exponent
    poly = polyfit(log(lags), log(tau), 1)
    #return Hurst Exponent from polyfit output
    return poly[0]*2.0
