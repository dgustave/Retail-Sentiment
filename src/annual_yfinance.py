import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime as dt
import yfinance as yf

def stockDataBY(symbol):
    
    ticks = yf.Ticker(symbol)
    currentDate = date.today()
    enddate = currentDate.strftime('%Y-%m-%d')
    five_yrs = currentDate - timedelta(days=1825)
    startdate = five_yrs.strftime('%Y-%m-%d')
    ydata_df = yf.download(symbol, start=startdate, end=enddate)
    date_list = pd.bdate_range(start=startdate, end=enddate, freq='BY')
    ticked_off = [ydata_df.loc[ydata_df.index == date] for date in date_list]
    ticker_5yr_df = pd.concat([ticked_off[0], ticked_off[1], ticked_off[2], ticked_off[3], ticked_off[4]])
    ticker_5yr_df.to_csv(f"../data/processed/{symbol}5yr.csv", index = False)
    return ydata_df, ticker_5yr_df