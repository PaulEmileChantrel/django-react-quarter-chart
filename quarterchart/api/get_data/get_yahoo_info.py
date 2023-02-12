import requests
import yfinance as yf
import pprint
from yahooquery import Ticker

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
def get_general_yahoo_info1(ticker:str)-> dict:
    #same function as above but using yahooquery
    stock = Ticker(ticker)
    asset_profile = stock.asset_profile
    asset_profile = asset_profile[ticker]

    earnings = stock.calendar_events
    earnings = earnings[ticker]['earnings']['earningsDate'][0]
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
    if ticker == 'AAPL':
        stock = Ticker(ticker)

        print(stock.summary_detail)
        # df = stock.income_statement('q')
        # df.to_csv('AAPL.csv')
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

if __name__ == '__main__':
    #main('TSLA')
    get_general_yahoo_info('TSLA')