import marketwatch 
import annual_yfinance
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date, timedelta, datetime as dt
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys   
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def generate_price_df(ticker, discountrate, marginrate): 
    symbol_df, ticker_df = stockDataBY(ticker)
    income_statement, balance_sheet, cashflow = get_financial_report(ticker)
    
    income_statement.index.rename('year', inplace=True)
    income_statement_cols_to_check= income_statement.columns
    # income_statement[income_statement_cols_to_check]= income_statement[income_statement_cols_to_check].replace({'-':''}, regex=True)
    income_statement[income_statement_cols_to_check]= income_statement[income_statement_cols_to_check].replace({'%':''}, regex=True)
    income_statement[income_statement_cols_to_check]= income_statement[income_statement_cols_to_check].replace({'B':''}, regex=True)
    income_statement[income_statement_cols_to_check]= income_statement[income_statement_cols_to_check].replace({'M':''}, regex=True)
    
    income = income_statement[['EPS (Basic)', 'EPS (Basic) Growth', 'Net Income', 'Interest Expense', 'EBITDA']]
    income[income.columns[0]] = income[income.columns[0]].map(lambda x: x.replace('(','-'))
    income[income.columns[0]] = income[income.columns[0]].map(lambda x: x.replace(')',''))
    income[income.columns[2]] = income[income.columns[2]].map(lambda x: x.replace('(','-'))
    income[income.columns[2]] = income[income.columns[2]].map(lambda x: x.replace(')',''))
    income[income.columns[4]] = income[income.columns[4]].map(lambda x: x.replace('(','-'))
    income[income.columns[4]] = income[income.columns[4]].map(lambda x: x.replace(')',''))
    income.rename(columns= {'EPS (Basic)': 'EPS', 'EPS (Basic) Growth': 'EPS Growth'}, inplace=True)
    income = income.apply(pd.to_numeric, errors='coerce')
    
    balance_sheet.index.rename('year', inplace=True)
    balance_sheet_cols_to_check = balance_sheet.columns
    # balance_sheet[balance_sheet_cols_to_check]= balance_sheet[balance_sheet_cols_to_check].replace({'-':''}, regex=True)
    balance_sheet[balance_sheet_cols_to_check]= balance_sheet[balance_sheet_cols_to_check].replace({'%':''}, regex=True)
    balance_sheet[balance_sheet_cols_to_check]= balance_sheet[balance_sheet_cols_to_check].replace({'B':''}, regex=True)
    balance_sheet[balance_sheet_cols_to_check]= balance_sheet[balance_sheet_cols_to_check].replace({'M':''}, regex=True)
    balance = balance_sheet[['Total Shareholders Equity', 'Total Shareholders Equity / Total Assets', 'Long-Term Debt']]
    income.rename(columns= {'Total Shareholders Equity / Total Assets': 'ROA', 'Long-Term Debt': 'Long Term Debt'}, inplace=True)
    balance = balance.apply(pd.to_numeric, errors='coerce')
    
    cashflow.index.rename('year', inplace=True)
    cashflow_cols_to_check = cashflow.columns
    # cashflow[cashflow_cols_to_check]= cashflow[cashflow_cols_to_check].replace({'-':''}, regex=True)
    cashflow[cashflow_cols_to_check]= cashflow[cashflow_cols_to_check].replace({'%':''}, regex=True)
    cashflow[cashflow_cols_to_check]= cashflow[cashflow_cols_to_check].replace({'B':''}, regex=True)
    cashflow[cashflow_cols_to_check]= cashflow[cashflow_cols_to_check].replace({'M':''}, regex=True)
#     cashflow[cashflow.columns[6]] = cashflow[cashflow.columns[6]].map(lambda x: x.replace('(','-'))
#     cashflow[cashflow.columns[6]] = cashflow[cashflow.columns[6]].map(lambda x: x.replace(')',''))
#     cashflow[cashflow.columns[7]] = cashflow[cashflow.columns[7]].map(lambda x: x.replace('(','-'))
#     cashflow[cashflow.columns[7]] = cashflow[cashflow.columns[7]].map(lambda x: x.replace(')',''))
#     cashflow[cashflow.columns[9]] = cashflow[cashflow.columns[9]].map(lambda x: x.replace('(','-'))
#     cashflow[cashflow.columns[9]] = cashflow[cashflow.columns[9]].map(lambda x: x.replace(')',''))
#     cashflow[cashflow.columns[12]] = cashflow[cashflow.columns[12]].map(lambda x: x.replace('(','-'))
#     cashflow[cashflow.columns[12]] = cashflow[cashflow.columns[12]].map(lambda x: x.replace(')',''))
#     cashflow[cashflow.columns[13]] = cashflow[cashflow.columns[13]].map(lambda x: x.replace('(','-'))
#     cashflow[cashflow.columns[13]] = cashflow[cashflow.columns[13]].map(lambda x: x.replace(')',''))
#     cashflow[cashflow.columns[14]] = cashflow[cashflow.columns[14]].map(lambda x: x.replace('(','-'))
#     cashflow[cashflow.columns[14]] = cashflow[cashflow.columns[14]].map(lambda x: x.replace(')',''))
#     cashflow[cashflow.columns[23]] = cashflow[cashflow.columns[23]].map(lambda x: x.replace('(','-'))
#     cashflow[cashflow.columns[23]] = cashflow[cashflow.columns[23]].map(lambda x: x.replace(')',''))
#     cashflow[cashflow.columns[25]] = cashflow[cashflow.columns[25]].map(lambda x: x.replace('(','-'))
#     cashflow[cashflow.columns[25]] = cashflow[cashflow.columns[25]].map(lambda x: x.replace(')',''))
#     cashflow[cashflow.columns[26]] = cashflow[cashflow.columns[26]].map(lambda x: x.replace('(','-'))
#     cashflow[cashflow.columns[26]] = cashflow[cashflow.columns[26]].map(lambda x: x.replace(')',''))
#     cashflow[cashflow.columns[30]] = cashflow[cashflow.columns[30]].map(lambda x: x.replace('(','-'))
#     cashflow[cashflow.columns[30]] = cashflow[cashflow.columns[30]].map(lambda x: x.replace(')',''))
    cashflow = cashflow.apply(pd.to_numeric, errors='coerce')
    
    financialreportingdf = pd.merge(income, balance, left_index=True, right_index=True)
    # Given the share price
    financialreportingdf.apply(pd.to_numeric, errors='coerce')
    dfprice = pd.DataFrame(columns =['ticker','annualgrowthrate','lasteps','futureeps'])
    pd.options.display.float_format = '{:20,.2f}'.format

#     # Find EPS Annual Compounded Growth Rate
#     annualgrowthrate =  income['EPS (Basic) Growth'].mean() #growth rate

    try:
        print(financialreportingdf['EPS'].iloc[0])
        print(financialreportingdf['EPS'].iloc[-1])
        annualgrowthrate =  np.rate(5, 0, -1*financialreportingdf['EPS'].iloc[0], financialreportingdf['EPS'].iloc[-1])
#         Find EPS Annual Compounded Growth Rate
#         annualgrowthrate =  income['EPS Growth'].mean() #growth rate
        print(annualgrowthrate)

        # Non Conservative
        lasteps = financialreportingdf['EPS'].tail(1).values[0] #presentvalue

        # conservative
#         lasteps = financialreportingdf.eps.mean()
        years  = 10 #period
        futureeps = abs(np.fv(annualgrowthrate,years,0,lasteps))
        dfprice.loc[0] = [ticker,annualgrowthrate,lasteps,futureeps]
        
    except:
        print('eps does not exist')


    ticker_df['year'] = pd.DatetimeIndex(ticker_df.index).year
    dfprice['peratio'] = ticker_df['Close'].tail(1).values[0]/financialreportingdf['EPS'].tail(1).values[0]
    dfprice['FV'] = dfprice['futureeps']*dfprice['peratio']
    dfprice['PV'] = abs(np.pv(discountrate,years,0,fv=dfprice['FV'].values))
    pd.options.display.float_format = '{:20,.2f}'.format
    dfprice.set_index('ticker', inplace=True)

    if dfprice['FV'].values[0] < 0:
        dfprice['marginprice'] = dfprice['PV']*(1-marginrate)
        
        dfprice['lastshareprice']= symbol_df.Close.tail(1).values[0]

        dfprice['decision'] = np.where((dfprice['lastshareprice']<dfprice['marginprice']),'BUY','SELL')
        daily_simple_returns = symbol_df['Adj Close'].pct_change()
        year_returns = daily_simple_returns.mean() * 250 
        asset = len(ticker)
        weights = np.random.random(asset)
        weights = weights / sum(weights)
        port_returns_expected = np.sum(weights * year_returns)
        dfprice['yrgrowth'] = (round(port_returns_expected * 100, 2))
        dfprice['growthdecision'] = np.where((dfprice['lastshareprice']<symbol_df['Adj Close'].tail(1).values[0]),'ShouldofBought','ShouldofSold')
        
    else:
#         dfprice['marginprice'] = 0
        dfprice['marginprice'] = dfprice['PV']*(1-marginrate)

#         dfprice['lastshareprice']= ticker_df.Close.tail(1).values[0]
        dfprice['lastshareprice']= symbol_df.Close.tail(1).values[0]

        dfprice['decision'] = np.where((dfprice['lastshareprice']<dfprice['marginprice']),'BUY','SELL')
        daily_simple_returns = symbol_df['Adj Close'].pct_change()
        year_returns = daily_simple_returns.mean() * 250 
        asset = len(ticker)
        weights = np.random.random(asset)
        weights = weights / sum(weights)
        port_returns_expected = np.sum(weights * year_returns)
        dfprice['yrgrowth'] = (round(port_returns_expected * 100, 2))
        dfprice['growthdecision'] = np.where((dfprice['lastshareprice']>ticker_df['Close'].tail(1).values[0]),'ShouldofBought','ShouldofSold')

    return dfprice