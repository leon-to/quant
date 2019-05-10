import pandas as pd
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
from scipy.stats import zscore
from scipy.signal import find_peaks

class Analyzer:
    def __init__(self, data_handler):
        self.data_hanlder = data_handler
        self.r = {} #result
        
    def coint(self):
        r = self.r
        symbols = self.data_hanlder.symbols
        close = self.data_hanlder.close
        
        # OLS 
        ols1 = sm.ols('%s ~ %s' %(symbols[0], symbols[1]), data=close).fit()
        ols2 = sm.ols('%s ~ %s' %(symbols[1], symbols[0]), data=close).fit()
        
        r_ols = r['ols'] = pd.DataFrame(index=ols1.resid.index)        
        r_ols['residual1'] = pd.DataFrame(ols1.resid)
        r_ols['residual2'] = pd.DataFrame(ols2.resid)
        r_ols[['z_score1']] = r_ols[['residual1']].apply(zscore)
        r_ols[['z_score2']] = r_ols[['residual2']].apply(zscore)
        
        # CAclose Test
        cadf1, p1, _ = coint(close[symbols[0]], close[symbols[1]])
        cadf2, p2, _ = coint(close[symbols[1]], close[symbols[0]])
        r['caclose'] = pd.DataFrame(
            data={'caclose':[cadf1, cadf2], 'pvalue':[p1, p2]}
        )
        
        # PLOT
        plt.style.use('seaborn-whitegrid')
        # close
        plt.figure()
        close.plot()
        # scatter 
        plt.figure()
        close.plot.scatter(symbols[0], symbols[1])
        # zscore 
        plt.figure()
        r['ols'][['z_score1', 'z_score2']].plot()
        
        plt.show()
        
        # print results
        print('CAclose Test')
        print(r['caclose'])
        