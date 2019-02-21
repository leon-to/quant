import pandas as pd
import numpy as np
import pandas_datareader.data as web
import datetime
import os
from backtest import Backtest
from data import HistoricCSVDataHandler
from execution import SimulatedExecutionHandler
from portfolio import Portfolio
from mac import MovingAverageCrossStrategy

def main():
    csv_dir = os.getcwd()
    symbol_list = ['AAPL']
    initial_capital = 100000.0
    hearbeat = 0.0
    start_date = datetime.datetime(1990,1,1,0,0,0)
    
    backtest = Backtest(
            csv_dir, symbol_list, initial_capital, hearbeat, 
            start_date, HistoricCSVDataHandler, SimulatedExecutionHandler,
            Portfolio, MovingAverageCrossStrategy)
    
    backtest.simulate_trading()

def read_csv():
    return pd.io.parsers.read_csv(
            'AAPL.csv',
            header=0, index_col=0, parse_dates=True
            )

def download_data():
    symbol = 'AAPL'
    source = 'yahoo'
    start = datetime.datetime(1990,1,1)
    end = datetime.datetime(2002,1,1)
    
    df = web.DataReader(symbol, source, start, end).rename(
            index = {'Index': 'datetime'},
            columns = {
                    'Index':'datetime',
                    'Open':'open',
                    'High':'high',
                    'Low':'low',
                    'Close':'close',
                    'Volume':'volume',
                    'Adj Close':'adj_close'
                    }
            ).to_csv('AAPL.csv')
    
main()
#df = read_csv()