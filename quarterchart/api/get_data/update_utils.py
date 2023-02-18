from ..models import Companie, CompanieBalanceSheet,CompanieCashFlow,CompanieIncomeStatement,CompanieInfo
from .get_yahoo_info import get_mkt_cap,get_next_earnings_date


    

def update_light_balance_sheet():
    companies = Companie.objects.all()
    for cpn in companies:
        balance_sheet = CompanieBalanceSheet.objects.filter(name=cpn).first()
        abl = balance_sheet.full_annual_balance_sheet
        qbl = balance_sheet.full_quarterly_balance_sheet
        
        abl_light = abl.loc[['Total Assets','Current Assets','Total Non Current Assets',"Total Debt",'Total Liabilities Net Minority Interest','Stockholders Equity']]
        qbl_light = qbl.loc[['Total Assets','Current Assets','Total Non Current Assets',"Total Debt",'Total Liabilities Net Minority Interest','Stockholders Equity']]
        balance_sheet.light_annual_balance_sheet = abl_light
        balance_sheet.light_quarterly_balance_sheet = qbl_light
       
        balance_sheet.save()

def update_light_income_statement():
    companies = Companie.objects.all()
    for cpn in companies:
        print(cpn.name)
        income_stmt = CompanieIncomeStatement.objects.filter(name=cpn).first()
        a_inc_stmt = income_stmt.full_annual_income_statement
        q_inc_stmt = income_stmt.full_quarterly_income_statement
        print(q_inc_stmt.index)
        a_inc_stmt_light = a_inc_stmt.loc[['Total Revenue','Gross Profit','Operating Expense','Operating Income','Net Income','Basic EPS','Normalized EBITDA']]
        q_inc_stmt_light = q_inc_stmt.loc[['Total Revenue','Gross Profit','Operating Expense','Operating Income','Net Income','Basic EPS','Normalized EBITDA']]
        income_stmt.light_annual_income_statement = a_inc_stmt_light
        income_stmt.light_quarterly_income_statement = q_inc_stmt_light
        
        income_stmt.save()

def update_light_cash_flow():
    companies = Companie.objects.all()
    for cpn in companies:
        cf = CompanieCashFlow.objects.filter(name=cpn).first()
        a_cf = cf.full_annual_cash_flow
        q_cf = cf.full_quarterly_cash_flow
        print(a_cf.index)
        print(a_cf)
        rows = set(['Operating Cash Flow','Investing Cash Flow','Financing Cash Flow','Operating Income','Net Income','Beginning Cash Position','End Cash Position','Free Cash Flow'])
        rows = list(rows.intersection(set(a_cf.index)))
        print(rows)
        a_cf_light = a_cf.loc[rows]
        q_cf_light = q_cf.loc[rows]
        cf.light_annual_cash_flow = a_cf_light
        cf.light_quarterly_cash_flow = q_cf_light
        
        
        cf.save()


def update_all_mkt_cap():
    companies = Companie.objects.all()
    for cpn in companies:
        ticker = cpn.ticker
        mkt_cap = get_mkt_cap(ticker)
        cpn.market_cap = mkt_cap
        cpn.save()
def update_earnings_date():
    companies = CompanieInfo.objects.all()
    for cpn in companies:
        ticker = cpn.ticker
        next_earnings_date = get_next_earnings_date(ticker)
        cpn.next_earnings_date = next_earnings_date
        cpn.save()

def save_all():
    #save all companies objects to redowload the data
    companies = Companie.objects.all()
    for cpn in companies:
        cpn.data_was_downloaded = False
        cpn.save()
def update_all():

    #update_light_cash_flow()
    #update_light_balance_sheet()
    update_light_income_statement()
    update_all_mkt_cap()
    update_earnings_date()
#update_all_mkt_cap()
#update_earnings_date()

#update_all() 
#save_all()

#load_companies()