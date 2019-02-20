import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web
import pprint
import statsmodels.tsa.stattools as ts


def plot_price_series (df, ts1, ts2):
    months = mdates.MonthLocator()
    fig, ax = plt.subplots()
    ax.plot(df.index, df[ts1], label=ts1)
    ax.plot(df.index, df[ts2], label=ts2)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(dt.datetime(2012,1,1), dt.datetime(2013,1,1))
    ax.grid(True)
    fig.autofmt_xdate()
    
    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('%s and %s Daily Prices' % (ts1, ts2))
    plt.legend()
    plt.show()
    
def plot_scatter_series (df, ts1, ts2):
    plt.xlabel ('%s Price ($)' % ts1)
    plt.ylabel ('%s Price ($)' % ts2)
    plt.title ('%s and %s Price Scatterplot' % (ts1, ts2))
    plt.scatter (df[ts1], df[ts2])
    plt.show()
    
def plot_residuals (df):
    months = mdates.MonthLocator()
    fig, ax = plt.subplots()
    ax.plot(df.index, df['res'], label='Residuals')
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(dt.datetime(2012,1,1), dt.datetime(2013,1,1))
    ax.grid(True)
    fig.autofmt_xdate()
    
    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('Residual Plot')
    plt.legend()
    
    plt.plot(df['res'])
    plt.show()