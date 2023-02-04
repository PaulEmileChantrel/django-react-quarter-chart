from django.db import models
from picklefield.fields import PickledObjectField
import pandas as pd
import time,json
from .get_data.get_yahoo_info import get_financial_yahoo_info,get_general_yahoo_info



def shrink_income_stmt(df):
    return df

def shrink_balance_sheet(df):
    return df

def shrink_cash_flow(df):
    return df



#Download data from Yahoo Finance and put it in the models
def download_info(compagnieModel):

    info_downloaded,finance_downloaded = False,False
    #general infos
    try:
        result = get_financial_yahoo_info(compagnieModel.ticker)
        
    except Exception as e:
        print(e)
    else:
        result = json.loads(result)

        compagnieModel.market_cap = result['marketCap']

        sector = result['sector']
        summary = result['longBusinessSummary']
        industry = result['industry']
        website = result['website']

        c_info = CompagnieInfo(ticker=compagnieModel.ticker,name=compagnieModel,sector=sector,summary=summary,industry=industry,website=website)
        c_info.save()
        info_downloaded = True

    try:
        income_stmt, quarterly_income_stmt, balance_sheet, quarterly_balance_sheet, cashflow, quarterly_cashflow = get_financial_yahoo_info(compagnieModel.ticker)

    except Exception as e:
        
        print(e)
    else:
        light_a_income_stmt = shrink_income_stmt(income_stmt)
        light_q_income_stmt = shrink_income_stmt(quartely_income_stmt)

        light_a_balance_sheet = shrink_balance_sheet(balance_sheet)
        light_q_balance_sheet = shrink_balance_sheet(quartely_balance_sheet)

        light_a_cashflow = shrink_cashflow(cashflow)    
        light_q_cashflow = shrink_cashflow(quartely_cashflow)

        comp_inc_stmt = CompagnieIncomeStatement(ticker=compagnieModel.ticker,name=compagnieModel,full_annual_income_statement=income_stmt,full_quarterly_income_statement=quarterly_income_stmt,light_annual_income_statement=light_a_income_stmt,light_quarterly_income_statement=light_q_income_stmt)
        comp_inc_stmt.save()
        comp_bal_stmt = CompagnieBalanceStatement(ticker=compagnieModel.ticker,name=compagnieModel,full_annual_balance_sheet=balance_sheet,full_quarterly_balance_sheet=quarterly_balance_sheet,light_annual_balance_sheet=light_a_balance_sheet,light_quarterly_balance_sheet=light_q_balance_sheet)
        comp_bal_stmt.save()
        comp_cashflow = CompagnieCashflowStatement(ticker=compagnieModel.ticker,name=compagnieModel,full_annual_cashflow=cashflow,full_quarter_quarterly_cashflow=quarterly_cashflow,light_annual_cashflow=light_a_cashflow,light_quarterly_cashflow=light_q_cashflow)
        comp_cashflow.save()

        finance_downloaded = True
    
    return info_downloaded and finance_downloaded


        
        





# Create your models here.
class Compagnies(models.Model):
    name = models.CharField(max_length=100,unique=True)
    ticker = models.CharField(max_length=6)
    data_was_downloaded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    image_link = models.CharField(max_length=250)
    market_cap = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def save(self):
        super(Compagnies, self).save()
        result = download_info(self)
        self.data_was_downloaded = result
        super(Compagnies, self).save()
        

class CompaniesInfo(models.Model):
    name = models.ForeignKey(Compagnies, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    summary = models.TextField()
    industry = models.CharField(max_length=100)
    website = models.CharField(max_length=250)
    last_updated_at = models.DateTimeField(auto_now_add=True)


class CompagnieBalanceSheet(models.Model):
    name = models.ForeignKey(Compagnies, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    full_annual_balance_sheet = PickledObjectField()
    full_quarterly_balance_sheet = PickledObjectField()
    light_annual_balance_sheet = PickledObjectField()
    light_quarterly_balance_sheet = PickledObjectField()
    last_updated_at = models.DateTimeField(auto_now=True)

class CompagnieIncomeStatement(models.Model):
    name = models.ForeignKey(Compagnies, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    full_annual_income_statement = PickledObjectField()
    full_quarterly_income_statement = PickledObjectField()
    light_annual_income_statement = PickledObjectField()
    light_quarterly_income_statement = PickledObjectField()
    last_updated_at = models.DateTimeField(auto_now=True)


class CompagnieCashFlowStatement(models.Model):
    name = models.ForeignKey(Compagnies, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    full_annual_cash_flow_statement = PickledObjectField()
    full_quarterly_cash_flow_statement = PickledObjectField()
    light_annual_cash_flow_statement = PickledObjectField()
    light_quarterly_cash_flow_statement = PickledObjectField()
    last_updated_at = models.DateTimeField(auto_now=True)
