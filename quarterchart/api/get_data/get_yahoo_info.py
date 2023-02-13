import requests
import yfinance as yf
import pprint
from yahooquery import Ticker
import datetime
import re
import pandas as pd
def main(ticker):
    stock = yf.Ticker(ticker)
    print(stock.basic_info)

    #finantials
    print("## Income Statement ##")
    print(stock.income_stmt)
    print(stock.quarterly_income_stmt)

    print("## Balance Sheet ##")
    print(stock.balance_sheet)
    print(stock.quarterly_balance_sheet)

    print("## Cash Flow ##")
    print(stock.cashflow)
    print(stock.quarterly_cashflow)

    print(stock.get_income_stmt())


def get_general_yahoo_info(ticker:str)-> dict:
    stock = yf.Ticker(ticker)
    infos = stock.fast_info
    marketCap = infos['market_cap']
    print(marketCap)
   
    infos = stock.info
    print(infos)
    return infos,marketCap

def get_next_earnings_date(ticker:str):
    stock = Ticker(ticker)
    earnings = stock.calendar_events
    
    earnings = earnings[ticker]['earnings']['earningsDate'][0]
    index = earnings.find('S')
    if index >0:
        earnings = earnings[:index-1]

    date_format = "%Y-%m-%d %H:%M"

    date_object = datetime.datetime.strptime(earnings, date_format)
    
    return earnings

def get_general_yahoo_info2(ticker:str)-> dict:
    #same function as above but using yahooquery
    stock = Ticker(ticker)
    asset_profile = stock.asset_profile
    asset_profile = asset_profile[ticker]

    earnings = stock.calendar_events
    earnings = earnings[ticker]['earnings']['earningsDate'][0]
    index = earnings.find('S')
    if index >0:
        earnings = earnings[:index-1]
    #for compatibility with yfinance results
    infos = {}
    infos['logo_link'] = ""
    infos['sector'] = asset_profile['sector']
    infos['longBusinessSummary'] = asset_profile['longBusinessSummary']
    infos['industry'] = asset_profile['industry']
    infos['website'] = asset_profile['website']
    infos['next_earnings_date'] = earnings
    marketCap = stock.summary_detail
    marketCap = marketCap[ticker]['marketCap']
    
    return infos,marketCap

def get_mkt_cap(ticker:str)-> dict:
    stock = yf.Ticker(ticker)
    infos = stock.fast_info
    
    marketCap = infos['market_cap']
    
    return marketCap

def get_financial_yahoo_info(ticker:str)-> dict:
    
    stock = yf.Ticker(ticker)

    #finantials
    print("## Income Statement ##")
    income_stmt = stock.income_stmt
    quarterly_income_stmt = stock.quarterly_income_stmt

    print("## Balance Sheet ##")
    balance_sheet = stock.balance_sheet
    quarterly_balance_sheet = stock.quarterly_balance_sheet

    print("## Cash Flow ##")
    cashflow = stock.cashflow
    quarterly_cashflow = stock.quarterly_cashflow

    #print(stock.get_income_stmt())
    return income_stmt, quarterly_income_stmt, balance_sheet, quarterly_balance_sheet, cashflow, quarterly_cashflow

def transform_df(df:pd.DataFrame)-> pd.DataFrame:
    df = df.T
    df.columns = list(df.loc['asOfDate'])
    print(df.loc['periodType'])
    if df.iloc[1,-1:].values[0] == 'TTM':
        df.columns = [*df.columns[:-1], 'TTM']
        #df.drop(columns = [col[0]],inplace=True)# dropping cols with TTM
        #df.rename(columns={col[0]:'TTM'}, inplace=True)
    #print(df.iloc[1,-1:].index)
    df.rename(index = lambda s : re.sub("([a-z])([A-Z])","\g<1> \g<2>",s), inplace=True)
    return df

def get_financial_yahoo_info2(ticker:str)-> list:
    stock = Ticker(ticker)
    #finantials
    print("## Income Statement ##")
    income_stmt = transform_df(stock.income_statement())
    quarterly_income_stmt = transform_df(stock.income_statement('q'))

    print("## Balance Sheet ##")
    balance_sheet = transform_df(stock.balance_sheet())
    quarterly_balance_sheet = transform_df(stock.balance_sheet('q'))

    print("## Cash Flow ##")
    cashflow = transform_df(stock.cash_flow())
    quarterly_cashflow = transform_df(stock.cash_flow('q'))
    print(quarterly_cashflow.loc['period Type'])
    #print(cashflow)
    return income_stmt, quarterly_income_stmt, balance_sheet, quarterly_balance_sheet, cashflow, quarterly_cashflow

    

if __name__ == '__main__':
    #main('TSLA')
    get_financial_yahoo_info2('TSLA')