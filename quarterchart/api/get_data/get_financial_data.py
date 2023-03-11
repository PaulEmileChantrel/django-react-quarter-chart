#get financial data with Financial Modelling Prep API

import requests
import pandas as pd
import json
from config import FINANCIAL_MODELLING_API_KEY
from get_yahoo_info import transform_df
API_KEY = FINANCIAL_MODELLING_API_KEY
api_url = 'https://financialmodelingprep.com/api/v3/'



def clean_inc_stmt_df(df):
    #rotate and change name 
    df = transform_df(df,date_col='date') 
    #renaming index row 
    df.rename(index = {'Revenue':'Total Revenue','Operating Expenses':'Operating Expense','Research And Development Expenses':'Research And Development','Selling General And Administrative Expenses':'Selling General And Administration','Ebitda':'Normalized EBITDA','Eps':'Basic EPS','Other Expenses':'Other OpEx'},inplace = True)
    #reverse cols
    return df[df.columns[::-1]]

def get_income_statement(ticker):
    
    annual_url = f'{api_url}income-statement/{ticker}?limit=120&apikey={FINANCIAL_MODELLING_API_KEY}' #max(38y?,company_max) years of data
    quarter_url = f'{api_url}income-statement/{ticker}?period=quarter&limit=400&apikey={FINANCIAL_MODELLING_API_KEY}'
   
    annual_df = pd.read_json(annual_url)
    quarter_df = pd.read_json(quarter_url)
    
    annual_df = clean_inc_stmt_df(annual_df)
    quarter_df = clean_inc_stmt_df(quarter_df)
    
    return annual_df, quarter_df
    
    
    

def get_balance_sheet(ticker):
    pass

def get_cash_flow(ticker):
    pass

if __name__ == '__main__':
    get_income_statement('AAPL')