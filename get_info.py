import requests
import yfinance as yf

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





if __name__ == '__main__':
    main('TSLA')