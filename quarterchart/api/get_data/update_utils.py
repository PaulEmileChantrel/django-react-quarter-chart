from ..models import Companie, CompanieBalanceSheet,CompanieCashFlow,CompanieIncomeStatement,CompanieInfo
from .get_yahoo_info import get_mkt_cap,get_next_earnings_date

from ..model_utils import shrink_income_stmt,shrink_balance_sheet,shrink_cashflow
    

def update_light_balance_sheet():
    companies = Companie.objects.all()
    for cpn in companies:
        print(cpn.ticker)
        balance_sheet = CompanieBalanceSheet.objects.filter(name=cpn).first()
        abl = balance_sheet.full_annual_balance_sheet
        qbl = balance_sheet.full_quarterly_balance_sheet
        #print(qbl.index)
        abl_light = shrink_balance_sheet(abl)
        qbl_light = shrink_balance_sheet(qbl)
        balance_sheet.light_annual_balance_sheet = abl_light
        balance_sheet.light_quarterly_balance_sheet = qbl_light
       
        balance_sheet.save()
        

def update_light_income_statement():
    companies = Companie.objects.all()
    for cpn in companies:
        print(cpn.ticker)
        income_stmt = CompanieIncomeStatement.objects.filter(name=cpn).first()
        a_inc_stmt = income_stmt.full_annual_income_statement
        q_inc_stmt = income_stmt.full_quarterly_income_statement
        #print(q_inc_stmt.index)
        a_inc_stmt_light = shrink_income_stmt(a_inc_stmt)
        q_inc_stmt_light = shrink_income_stmt(q_inc_stmt)
        income_stmt.light_annual_income_statement = a_inc_stmt_light
        income_stmt.light_quarterly_income_statement = q_inc_stmt_light
        
        income_stmt.save()
        

def update_light_cash_flow():
    companies = Companie.objects.all()
    for cpn in companies:
        print(cpn.ticker)
        cf = CompanieCashFlow.objects.filter(name=cpn).first()
        a_cf = cf.full_annual_cash_flow
        q_cf = cf.full_quarterly_cash_flow
        #print(a_cf.index)
        
        a_cf_light = shrink_cashflow(a_cf)
        q_cf_light = shrink_cashflow(q_cf)
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
    #update_all_mkt_cap()
    #update_earnings_date()
#update_all_mkt_cap()
#update_earnings_date()

#update_all() 
#save_all()

#load_companies()