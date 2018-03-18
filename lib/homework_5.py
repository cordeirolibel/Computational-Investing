
# ## Homework 5
# http://wiki.quantsoftware.org/index.php?title=CompInvesti_Homework_5


from lib import DataAccess as da
from lib import qsdateutil as du
from lib import EventProfiler as ep
from lib import homework_2 as h2
from lib import homework_3 as h3
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def bollinger_bands(closes, days=20, alpha_std = 2, plot = True):
    dict_out = dict()
    k = 1
    n = len(closes)
    for symbol in closes:
    
        # Create Dataframe
        df = pd.DataFrame()
        df['price'] = closes[symbol]
        df['average'] = closes[symbol].rolling(window=days, center=False).mean() 
        std = closes[symbol].rolling(window=days,center=False).std()*alpha_std 
        df['std_up'] = df['average']+std
        df['std_down'] = df['average']-std
        df['bollinger_val'] = (df['price'] - df['average']) / (std)
        
        #Operations
        df['op'] = ''
        for i in range(len(df)-1):
            if df['bollinger_val'][i+1]>=1 and df['bollinger_val'][i]<1:
                df['op'].iloc[i+1]= 'Sell'
            elif df['bollinger_val'][i+1]<=-1 and df['bollinger_val'][i]>-1:
                df['op'].iloc[i+1]='Buy'
        
        if plot:
            #plot
            plt.figure(figsize=(15,5))
            plt.title(symbol)
            plt.ylabel('Adjusted Close')
            plt.plot(df.index,df['price'], lw=2)
            plt.plot(df.index,df['std_up'],c='gray')
            plt.plot(df.index,df['std_down'],c='gray')
            plt.fill_between(df.index, df['std_down'], df['std_up'],  facecolor='gray',alpha=0.2)
            #operations lines
            for date in df[df['op']=='Buy'].index:
                plt.axvline(x=date,c='g',alpha=0.2)
            for date in df[df['op']=='Sell'].index:
                plt.axvline(x=date,c='r',alpha=0.2)
            
            #Bollinger plot
            plt.figure(figsize=(15,5))
            plt.title(symbol)
            plt.ylabel('Bollinger Faeture')
            plt.plot(df.index,df['bollinger_val'], lw=2)
            plt.plot(df.index,np.ones(len(df)), c='gray')
            plt.plot(df.index,-np.ones(len(df)), c='gray')
            plt.fill_between(df.index,np.ones(len(df)), -np.ones(len(df)),  facecolor='gray',alpha=0.2)
            #operations lines
            for date in df[df['op']=='Buy'].index:
                plt.axvline(x=date,c='g',alpha=0.2)
            for date in df[df['op']=='Sell'].index:
                plt.axvline(x=date,c='r',alpha=0.2)
            
            
            plt.show()
        else:
            print(k,'/',n-1)
            k+=1
        dict_out[symbol] = df
    return dict_out


# ### Simple Move Average SMA

def simple_move_average(closes, days=20):
    dict_out = dict()
    for symbol in closes:
    
        # Create Dataframe
        df = pd.DataFrame()
        df['price'] = closes[symbol]
        df['average'] = closes[symbol].rolling(window=days, center=False).mean() 
        
        #Operations
        df['op'] = ''
        for i in range(len(df)-1):
            if df['price'][i+1]>=df['average'][i+1] and df['price'][i]<df['average'][i]:
                df['op'].iloc[i+1]= 'Buy'
            elif df['price'][i+1]<=df['average'][i+1] and df['price'][i]>df['average'][i]:
                df['op'].iloc[i+1]='Sell'
        
        #plot
        plt.figure(figsize=(15,5))
        plt.title(symbol)
        plt.ylabel('Adjusted Close')
        plt.plot(df.index,df['price'], lw=2)
        plt.plot(df.index,df['average'], lw=2,c='r')
        #operations lines
        for date in df[df['op']=='Buy'].index:
            plt.axvline(x=date,c='g',alpha=0.2)
        for date in df[df['op']=='Sell'].index:
            plt.axvline(x=date,c='r',alpha=0.2)
        
        plt.show()
        dict_out[symbol] = df
    return dict_out

# ###  Moving Average Convergence Divergence MACD

def moving_average_convergence_divergence(closes, days1=30, days2=15):
    dict_out = dict()
    for symbol in closes:
    
        # Create Dataframe
        df = pd.DataFrame()
        df['price'] = closes[symbol]
        df['average1'] = closes[symbol].rolling(window=days1, center=False).mean() 
        df['average2'] = closes[symbol].rolling(window=days2, center=False).mean() 
        df['macd'] = df['average2']-df['average1']
        
        #Operations
        df['op'] = ''
        for i in range(len(df)-1):
            if df['average2'][i+1]>=df['average1'][i+1] and df['average2'][i]<df['average1'][i]:
                df['op'].iloc[i+1]= 'Buy'
            elif df['average2'][i+1]<=df['average1'][i+1] and df['average2'][i]>df['average1'][i]:
                df['op'].iloc[i+1]='Sell'
        
        #plot
        f, (ax1,ax2) = plt.subplots(2,sharex=True,figsize=(15,7), gridspec_kw = {'height_ratios':[5, 1]})
        ax1.set_title(symbol)
        ax1.set_ylabel('Adjusted Close')
        ax1.plot(df.index,df['price'], lw=1,c='k',alpha=0.7)
        ax1.plot(df.index,df['average1'], lw=2,c='firebrick')
        ax1.plot(df.index,df['average2'], lw=2,c='b')
        #macd
        ax2.bar(df.index,df['macd'],color='darkgray')
        ax2.axhline(y=0, color='k',lw=0.5)
        #operations lines
        for date in df[df['op']=='Buy'].index:
            ax1.axvline(x=date,c='g',alpha=0.2)
            ax2.axvline(x=date,c='g',alpha=0.2)
        for date in df[df['op']=='Sell'].index:
            ax1.axvline(x=date,c='r',alpha=0.2)
            ax2.axvline(x=date,c='r',alpha=0.2)
            
        f.subplots_adjust(hspace=0)
        plt.show()
        dict_out[symbol] = df
    return dict_out
