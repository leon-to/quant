import pandas as pd
import pandas_datareader.data as web

class DataHandler:
    def __init__(self):
        self.symbols = None
        self.data = {} # raw data parsed from source
        self.close = None # (adjusted) close price
        self.single = {} # a single symbol OHLC
    
    def scrap_pddr_data(self, symbols, source, start, end):
        self.symbols = symbols
        self.data = web.DataReader(symbols, source, start, end)
        self.close = self.data['Adj Close'] 
        
        for symbol in symbols:
            self.single[symbol] = self.data.xs(symbol, 1, 1)
            
    def read_data(self, symbols):
        self.symbols = symbols
        for symbol in symbols:
            self.data[symbol] = pd.read_csv(
                                    './data/%s' % symbol, 
                                    header=0, 
                                    index_col=0, 
                                    parse_dates=True
                                )