
# ## Homework 4
# http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_4


from lib import DataAccess as da
from lib import qsdateutil as du
from lib import EventProfiler as ep
from lib import homework_2 as h2
from lib import homework_3 as h3
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



def evento2orders(matrix_event,orders,buy_days=0,sell_days=5,shares=100):
    
    #organize buy and sell days for all dates
    matrix_event['buy_day'] = matrix_event.index
    matrix_event['sell_day'] = matrix_event.index
    matrix_event['buy_day'] = matrix_event['buy_day'].shift(-buy_days)
    matrix_event['sell_day'] = matrix_event['sell_day'].shift(-sell_days)
    
    # Create Buy and Sell orders
    out = list()
    for column in matrix_event:
        if column=='buy_day' or column=='sell_day':
            continue
        symbol = matrix_event[column]
        for date, event in symbol.dropna().iteritems():
            buy_day = matrix_event['buy_day'][date]
            sell_day = matrix_event['sell_day'][date]
            if buy_day==buy_day:
                #[year, month, day, symbol, op, n_shares]
                out.append([buy_day.year,buy_day.month,buy_day.day,column,'Buy',shares])
            if sell_day==sell_day:           
                out.append([sell_day.year,sell_day.month,sell_day.day,column,'Sell',shares])
    
    # To Dataframe
    col = ['year','month','day','symbol','op','n_shares']
    df_od = pd.DataFrame(out,columns = col)
    df_od = df_od.sort_values(by=['year', 'month', 'day'])
    df_od = df_od.reset_index(drop=True)
    df_od.to_csv('data/orders/'+orders+'.csv',index = False)
    
    del matrix_event['buy_day']
    del matrix_event['sell_day']
    return df_od

