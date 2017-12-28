# https://github.com/cordeirolibel/         

# ## Homework 1
# http://wiki.quantsoftware.org/index.php?title=CompInvestI_Homework_1<br>
# http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_1

import pandas_datareader.data as web
from lib import DataAccess as da
from lib import qsdateutil as du
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
get_ipython().magic(u'matplotlib inline')


# __Inputs:__<br>
# Start date (e.g. '01/01/2010')<br> 
# End date<br>
# Symbols for for equities (e.g., GOOG, AAPL, GLD, XOM)<br>
# Allocations to the equities at the beginning of the simulation (e.g., 0.2, 0.3, 0.4, 0.1)<br>
# __Return:__<br>
# Standard deviation of daily returns of the total portfolio<br>
# Average daily return of the total portfolio<br>
# Sharpe ratio (Always assume you have 252 trading days in an year. And risk free rate = 0) of the total portfolio<br>
# Cumulative return of the total portfolio<br>





def simulate(startdate,enddate,symbols,allocations):
    c_dataobj = da.DataAccess('Yahoo')
    
    #date
    dt_timeofday = dt.timedelta(hours=16)
    timestamps = du.getNYSEdays(startdate, enddate, dt_timeofday)
    
    #data
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(timestamps, symbols, keys)
    d_data = dict(zip(keys, ldf_data))
    
    #normalize
    df = d_data["close"]/d_data["close"].iloc[0]
    #allocations
    for a,s in zip(allocations, symbols):
        df[s] = df[s]*a
    
    #new columns
    df['comu_ret'] = [sum(row) for _,row in df.iterrows()]
    df['daily_ret'] = [0.0]+[df['comu_ret'][i+1]/df['comu_ret'][i]-1 for i in range(len(df)-1)]
    
    #the returns 
    vol = np.std(df['daily_ret'])
    daily_ret_avg = df['daily_ret'].mean()
    sharpe = np.sqrt(252)*daily_ret_avg/vol
    cum_ret = df['comu_ret'][-1]-1

    return vol, daily_ret_avg, sharpe, cum_ret



# ## Extra challenges
# Find the best allocations using optimization algorithms.

from scipy.optimize import minimize


# e.g. <br>
# if x = [1,2] means:<br>
# y[1] = 1y[0] <br>
# y[2] = 2y[0]<br>
# sum(y) = 1<br>
# y[0],y[1],y[2]>0<br>
#    then return [0.25,0.25,0.5]

def relationTOmax1(x):
    x = np.array([1]+list(abs(x)),dtype = float)
    return x/x.sum()


# Function to minimize:

def f(x,startdate,enddate,symbols):
    allocations = relationTOmax1(x)
    _,_,sharpe,_ = simulate(startdate,enddate,symbols,allocations)
    return 1/sharpe



