#get financial data with Financial Modelling Prep API

import requests
import pandas as pd
import json
from config import FINANCIAL_MODELLING_API_KEY
from get_yahoo_info import transform_df
API_KEY = FINANCIAL_MODELLING_API_KEY
api_url = 'https://financialmodelingprep.com/api/v3'



def clean_df(df,rename_dict):
    #rotate and change name 
    df = transform_df(df,date_col='date') 
    #renaming index row 
    df.rename(index = rename_dict,inplace = True)
    #reverse cols
    return df[df.columns[::-1]]

def get_income_statement(ticker):
    
    annual_url = f'{api_url}/income-statement/{ticker}?limit=120&apikey={FINANCIAL_MODELLING_API_KEY}' #max(38y?,company_max) years of data
    quarter_url = f'{api_url}/income-statement/{ticker}?period=quarter&limit=400&apikey={FINANCIAL_MODELLING_API_KEY}'
   
    annual_df = pd.read_json(annual_url)
    quarter_df = pd.read_json(quarter_url)
    
    rename_dict = {'Ebitda':'EBITDA','Eps':'EPS'}
    annual_df = clean_df(annual_df,rename_dict)
    quarter_df = clean_df(quarter_df,rename_dict)
    
    return annual_df, quarter_df
    


def get_balance_sheet(ticker):
    annual_url = f'{api_url}/balance-sheet-statement/{ticker}?limit=120&apikey={FINANCIAL_MODELLING_API_KEY}' #max(38y?,company_max) years of data
    quarter_url = f'{api_url}/balance-sheet-statement/{ticker}?period=quarter&limit=400&apikey={FINANCIAL_MODELLING_API_KEY}'
   
    annual_df = pd.read_json(annual_url)
    quarter_df = pd.read_json(quarter_url)
    
    
    rename_dict = {}
    annual_df = clean_df(annual_df,rename_dict)
    quarter_df = clean_df(quarter_df,rename_dict)
       
    return annual_df, quarter_df

def get_cash_flow(ticker):
    annual_url = f'{api_url}/cash-flow-statement/{ticker}?limit=120&apikey={FINANCIAL_MODELLING_API_KEY}' #max(38y?,company_max) years of data
    quarter_url = f'{api_url}/cash-flow-statement/{ticker}?period=quarter&limit=400&apikey={FINANCIAL_MODELLING_API_KEY}'
   
    annual_df = pd.read_json(annual_url)
    quarter_df = pd.read_json(quarter_url)
    
    rename_dict = {}
    annual_df = clean_df(annual_df,rename_dict)
    quarter_df = clean_df(quarter_df,rename_dict)
    print(annual_df) 
    return annual_df, quarter_df


def get_financials(ticker):
    annual_income_stmt,quarter_income_stmt = get_income_statement(ticker)
    annual_balance_st,quarter_balance_st = get_balance_sheet(ticker)
    annual_cashflow,quarter_cashflow = get_cash_flow(ticker)
    
    return annual_income_stmt,quarter_income_stmt,annual_balance_st,quarter_balance_st,annual_cashflow,quarter_cashflow
if __name__ == '__main__':
    get_cash_flow('AAPL')