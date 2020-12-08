
import sys 
import os
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from flask import request 
import psycopg2
# Import SQL Alchemy
import sqlalchemy
from sqlalchemy import create_engine, inspect, func
# Import and establish Base for which classes will be constructed 
# Import modules to declare columns and column data types
from sqlalchemy import Column, Integer, String, Float, ForeignKey
# Import and establish Base for which classes will be constructed 
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# Session is a temporary binding to our DB
from sqlalchemy.orm import Session
from psycopg2.extensions import register_adapter, AsIs
from datetime import date, timedelta, datetime as dt

class stockTable(Base):
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True)
    TIMESTAMP = Column(String(30))
    OPEN = Column(Float)
    HIGH = Column(Float)
    LOW = Column(Float)
    CLOSE = Column(Float)
    TURNOVER = Column(Float)
    VOLATILITY = Column(Float)

def updateTable(request):
    if request.method == 'POST':
        symbol = request.form.get('symb') 
        stockstdate = request.form.get('start')
        stockedate = request.form.get('end')
        stock_df = stockData(symbol)
        engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/stock_db')
        connection = engine.connect()
        session = Session(bind=engine)
        Base.metadata.drop_all(engine)
        # Create tables within the database
        Base.metadata.create_all(connection)
        try:
                for row in stock_df.iterrows():

                    stock = stockTable(TIMESTAMP=row[1][0], OPEN=row[1][1],HIGH=row[1][2],LOW=row[1][3], CLOSE=row[1][4],
                                    TURNOVER=row[1][5],VOLATILITY=row[1][6])
                    session.add(stock)
                #   session.flush()
                    print(stock)
                    session.commit()

        except (Exception, psycopg2.Error) as error:
            print("Error in update operation", error)

        finally:
            # closing database connection.
            if (connection):
                session.close()
                connection.close()
                print("PostgreSQL connection is closed")



def stockData(symbol):
    ticks = yf.Ticker(symbol)
    currentDate = date.today()
    enddate = currentDate.strftime('%Y-%m-%d')
    four_yrs = currentDate - timedelta(days=1460)
    startdate = four_yrs.strftime('%Y-%m-%d')
    ydata_df = yf.download(symbol, start=startdate, end=enddate)
    ydata_df.columns = ["OPEN", "HIGH", "LOW", "CLOSE", "Adj Close", "Volume"]
    daily_close = ydata_df[['Adj Close']]
    daily_pct_change = daily_close.pct_change()
    daily_pct_change.fillna(0, inplace=True)
    daily_pct_change
    min_periods = 2

    # Calculate the volatility
    vol = (daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods))
    vol.columns = ["VOLATILITY"]
    vol.fillna(0, inplace=True)
    out = ticks.info.get('sharesOutstanding')
    daily_turnover = ydata_df[['Volume']]
    turnover = (daily_turnover/out) 
    turnover.columns = ["TURNOVER"]

    ydata_df["TURNOVER"] = turnover["TURNOVER"]
    ydata_df["VOLATILITY"] = vol["VOLATILITY"]
    data_df = ydata_df.drop(columns = ["Adj Close", "Volume"])

    df = data_df.reset_index()
    df = df.rename(columns = {"Date": "TIMESTAMP"})

    new_df = df.round({"OPEN": 2, "HIGH": 2, "LOW": 2, "CLOSE": 2})
    new_df


    TIMESTAMP = new_df["TIMESTAMP"].to_list()
    OPEN = new_df["OPEN"].to_list()
    HIGH = new_df["HIGH"].to_list()
    LOW = new_df["LOW"].to_list()
    CLOSE = new_df["CLOSE"].to_list()
    TURNOVER = new_df["TURNOVER"].to_list()
    VOLATILITY = new_df["VOLATILITY"].to_list()
    vol_dict = {"TIMESTAMP": TIMESTAMP, "OPEN": OPEN, "HIGH": HIGH, "LOW ": LOW , "CLOSE": CLOSE, "TURNOVER": TURNOVER, "VOLATILITY": VOLATILITY,}
    ticker_df = pd.DataFrame(vol_dict)
    ticker_df.to_csv(f"../data/processed/stockdata.csv", index = False)
    return ticker_df

