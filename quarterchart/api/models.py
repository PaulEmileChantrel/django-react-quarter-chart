from django.db import models
from picklefield.fields import PickledObjectField
import pandas as pd
import time,json
from .get_data.get_yahoo_info import get_financial_yahoo_info,get_general_yahoo_info



def shrink_income_stmt(df):
    return df.loc[['Total Revenue','Gross Profit','Operating Expense','Operating Income','Net Income','Basic EPS','Normalized EBITDA']]

def shrink_balance_sheet(df):
    return df.loc[['Total Assets','Current Assets','Total Non Current Assets',"Total Debt",'Total Liabilities Net Minority Interest','Stockholders Equity']]
    

def shrink_cashflow(df):
    rows = set(['Operating Cash Flow','Investing Cash Flow','Financing Cash Flow','Operating Income','Net Income','Beginning Cash Position','End Cash Position','Free Cash Flow'])
    rows = list(rows.intersection(set(a_cf.index)))
    return df.loc[rows]



#Download data from Yahoo Finance and put it in the models
def download_info(companieModel):

    info_downloaded,finance_downloaded = False,False
    #general infos
    try:
        infos,market_cap = get_general_yahoo_info(companieModel.ticker)
        
    except Exception as e:
        print(e)
    else:
        
        companieModel.market_cap = market_cap
        print(infos)
        companieModel.image_link = infos['logo_link']
        sector = infos['sector']
        summary = infos['longBusinessSummary']
        industry = infos['industry']
        website = infos['website']

        c_info = CompanieInfo(ticker=companieModel.ticker,name=companieModel,sector=sector,summary=summary,industry=industry,website=website)
        c_info.save()
        info_downloaded = True

    try:
        income_stmt, quarterly_income_stmt, balance_sheet, quarterly_balance_sheet, cashflow, quarterly_cashflow = get_financial_yahoo_info(companieModel.ticker)
        
    except Exception as e:
        
        print('error : ',e)
    else:
        light_a_income_stmt = shrink_income_stmt(income_stmt)
        light_q_income_stmt = shrink_income_stmt(quarterly_income_stmt)

        light_a_balance_sheet = shrink_balance_sheet(balance_sheet)
        light_q_balance_sheet = shrink_balance_sheet(quarterly_balance_sheet)

        light_a_cashflow = shrink_cashflow(cashflow)    
        light_q_cashflow = shrink_cashflow(quarterly_cashflow)

        comp_inc_stmt = CompanieIncomeStatement(ticker=companieModel.ticker,name=companieModel,full_annual_income_statement=income_stmt,full_quarterly_income_statement=quarterly_income_stmt,light_annual_income_statement=light_a_income_stmt,light_quarterly_income_statement=light_q_income_stmt)
        comp_inc_stmt.save()
        comp_bal_stmt = CompanieBalanceSheet(ticker=companieModel.ticker,name=companieModel,full_annual_balance_sheet=balance_sheet,full_quarterly_balance_sheet=quarterly_balance_sheet,light_annual_balance_sheet=light_a_balance_sheet,light_quarterly_balance_sheet=light_q_balance_sheet)
        comp_bal_stmt.save()
        comp_cashflow = CompanieCashFlow(ticker=companieModel.ticker,name=companieModel,full_annual_cash_flow=cashflow,full_quarterly_cash_flow=quarterly_cashflow,light_annual_cash_flow=light_a_cashflow,light_quarterly_cash_flow=light_q_cashflow)
        comp_cashflow.save()

        finance_downloaded = True
    
    return info_downloaded and finance_downloaded


        
        





# Create your models here.
class Companie(models.Model):
    name = models.CharField(max_length=100,unique=True)
    ticker = models.CharField(max_length=6,unique=True)
    data_was_downloaded = models.BooleanField(default=False)
    created_at_date = models.DateTimeField(auto_now_add=True)
    image_link = models.CharField(max_length=250,default='')
    market_cap = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def save(self):
        super(Companie, self).save()
        if not self.data_was_downloaded:
            result = download_info(self)
            self.data_was_downloaded = result
            super(Companie, self).save()
        

class CompanieInfo(models.Model):
    name = models.ForeignKey(Companie,related_name='compagnie_info', on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    summary = models.TextField()
    industry = models.CharField(max_length=100)
    website = models.CharField(max_length=250)
    last_updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name.name +' Infos'
class CompanieBalanceSheet(models.Model):
    name = models.ForeignKey(Companie, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    full_annual_balance_sheet = PickledObjectField()
    full_quarterly_balance_sheet = PickledObjectField()
    light_annual_balance_sheet = PickledObjectField()
    light_quarterly_balance_sheet = PickledObjectField()
    last_updated_at = models.DateTimeField(auto_now=True)
    full_num_col = models.IntegerField(default=0)
    full_num_row = models.IntegerField(default=0)
    light_num_col = models.IntegerField(default=0)
    light_num_row = models.IntegerField(default=0)
    def save(self):
        self.full_num_col = self.full_annual_balance_sheet.shape[1]
        self.full_num_row = self.full_annual_balance_sheet.shape[0]
        self.light_num_col = self.light_annual_balance_sheet.shape[1]
        self.light_num_row = self.light_annual_balance_sheet.shape[0]
        super(CompanieBalanceSheet, self).save()
    
    def __str__(self):
        return self.name.name +' Balance Sheet'


class CompanieIncomeStatement(models.Model):
    name = models.ForeignKey(Companie, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    full_annual_income_statement = PickledObjectField()
    full_quarterly_income_statement = PickledObjectField()
    light_annual_income_statement = PickledObjectField()
    light_quarterly_income_statement = PickledObjectField()
    last_updated_at = models.DateTimeField(auto_now=True)
    full_num_col = models.IntegerField(default=0)
    full_num_row = models.IntegerField(default=0)
    light_num_col = models.IntegerField(default=0)
    light_num_row = models.IntegerField(default=0)

    def save(self):
        self.full_num_col = self.full_annual_income_statement.shape[1]
        self.full_num_row = self.full_annual_income_statement.shape[0]
        self.light_num_col = self.light_annual_income_statement.shape[1]
        self.light_num_row = self.light_annual_income_statement.shape[0]
        super(CompanieIncomeStatement, self).save()
    def __str__(self):
        return self.name.name+ ' Income Statement'
class CompanieCashFlow(models.Model):
    name = models.ForeignKey(Companie, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    full_annual_cash_flow = PickledObjectField()
    full_quarterly_cash_flow = PickledObjectField()
    light_annual_cash_flow = PickledObjectField()
    light_quarterly_cash_flow = PickledObjectField()
    last_updated_at = models.DateTimeField(auto_now=True)
    full_num_col = models.IntegerField(default=0)
    full_num_row = models.IntegerField(default=0)
    light_num_col = models.IntegerField(default=0)
    light_num_row = models.IntegerField(default=0)

    def save(self):
        self.full_num_col = self.full_annual_cash_flow.shape[1]
        self.full_num_row = self.full_annual_cash_flow.shape[0]
        self.light_num_col = self.light_annual_cash_flow.shape[1]
        self.light_num_row = self.light_annual_cash_flow.shape[0]
        super(CompanieCashFlow, self).save()

    def __str__(self):
        return self.name.name+ ' Cash Flow'