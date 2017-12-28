# https://github.com/cordeirolibel/         

# # Homework 2
# http://wiki.quantsoftware.org/index.php?title=CompInvestI_Homework_2<br>
# http://wiki.quantsoftware.org/index.php?title=QSTK_Tutorial_9


import pandas_datareader.data as web
from lib import DataAccess as da
from lib import qsdateutil as du
from lib import EventProfiler as ep
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
get_ipython().magic(u'matplotlib inline')


def event5(df_closes, cut_off = 5.0):
    df_events = df_closes.copy()*np.NAN
    n = len(df_closes)
    for col in df_closes:
        for i in range(n-1):
            if df_closes[col][i+1]<cut_off and df_closes[col][i]>= cut_off:# and i>20 and i<(n-20):
                df_events[col][i+1] = 1
    return df_events


# ## Extra challenges
# Find the best cut-off price to maximize the return 5 days after the event.


from scipy.optimize import minimize


# Get std/mean of all returns in 'days=5' days after the event. <br>
# The less return is the best.


def meanReturn5days(df_events_arg,data,days = 5):
    #copys
    df_events = df_events_arg.copy()
    closes = data['close'].copy()
    
    # Removing the starting and the end events
    df_events.iloc[0:days] = np.NaN
    df_events.iloc[-days:] = np.NaN
    
    # Get all returns in 'days' days after the event
    ls_ret = list()
    for i, s_sym in enumerate(df_events.columns):
        for j, dt_date in enumerate(df_events.index):
            if df_events[s_sym][dt_date] == 1:
                ls_ret.append(closes[s_sym][j + days])
    
    return np.std(ls_ret)/np.mean(ls_ret)


# Function to minimize:

def f(x,data):
    df_events = event5(data['actual_close'],cut_off = x)
    return meanReturn5days(df_events,data)

