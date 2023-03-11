#get financial data with Financial Modelling Prep API

import requests
import pandas as pd
import json
from config import FINANCIAL_MODELLING_API_KEY
from get_yahoo_info import transform_df
API_KEY = FINANCIAL_MODELLING_API_KEY
api_url = 'https://financialmodelingprep.com/api/v3/'

def get_income_statement(ticker):
    
    annual_url = f'{api_url}income-statement/{ticker}?limit=120&apikey={FINANCIAL_MODELLING_API_KEY}' #max(38y?,company_max) years of data
    quarter_url = f'{api_url}income-statement/{ticker}?period=quarter&limit=400&apikey={FINANCIAL_MODELLING_API_KEY}'
   
    df = pd.read_json(annual_url)
    df = transform_df(df,date_col='date') #format the df 
    df.to_csv('annual_url.csv')
    print(df)
    

def get_balance_sheet(ticker):
    pass

def get_cash_flow(ticker):
    pass

if __name__ == '__main__':
    get_income_statement('AAPL')