from django.db import models
from picklefield.fields import PickledObjectField
from .get_data.get_yahoo_info import get_general_yahoo_info2,get_financial_yahoo_info2,get_mkt_cap,get_share_price,get_next_earnings_date
from .get_data.get_financial_data import get_financials
import datetime
from config import API_KEY
import pytz
from .model_utils import *
import pdb
import traceback
def convertInUSD(currency):
   #1) check db for currency value
   #2) if currency value is not in db, get it from api
   currency_query = Currency.objects.filter(name=currency)
   print(currency_query)
   if currency_query.exists():
      currency_in_db = currency_query.first()
      today = datetime.datetime.now()
      yesterday = today - datetime.timedelta(days=1)
      last_currency_update = currency_in_db.last_updated_at
      utc=pytz.UTC
      #print(utc.localize(yesterday), utc.localize(last_currency_update))
      if last_currency_update > utc.localize(yesterday):
         return currency_in_db.value
      else:
          currency_value = api_call(currency)
          currency_in_db.value = currency_value
          currency_in_db.last_updated_at = datetime.datetime.now()
          currency_in_db.save()
          return currency_value
   currency_value = api_call(currency)
   currency_in_db = Currency(name=currency,ticker=currency, value=currency_value,last_updated_at=datetime.datetime.now())
   currency_in_db.save()
   return currency_value
      
def update_companies():
    
    companies = Companie.objects.all()
    for cpn in companies:
        ticker = cpn.ticker
        #print(ticker)
        try:
            mkt_cap = get_mkt_cap(ticker)
            share,var,currency = get_share_price(ticker)
        except:
            print(f"error for {ticker}")
        else:
            if currency != 'USD':
                mult = convertInUSD(currency)
                mkt_cap*=mult
                share*=mult
            cpn.market_cap = mkt_cap
            cpn.share_price = share
            cpn.one_day_variation = var
            cpn.save()
        

   


#Download data from Yahoo Finance and put it in the models
def download_info(companieModel):

    info_downloaded,finance_downloaded = False,False
    #general infos
    try:
        infos,market_cap,share_price,currency,one_day_variation = get_general_yahoo_info2(companieModel.ticker)
        
    except Exception as e:
        print(e)
    else:
        if currency!='USD':
            mult = convertInUSD(currency)
            market_cap*=mult
            share_price*=mult
        companieModel.market_cap = market_cap
        #print(infos)
        companieModel.image_link = f'/static/images/company_logo/{companieModel.ticker.lower()}.webp'
        companieModel.share_price = share_price
        companieModel.one_day_variation = one_day_variation
        sector = infos['sector']
        summary = infos['longBusinessSummary']
        industry = infos['industry']
        website = infos['website']
        if 'next_earnings_date' in infos:
            next_earnings_date = infos['next_earnings_date']
        else:
            next_earnings_date = yesterday()

        c_info = CompanieInfo(ticker=companieModel.ticker,name=companieModel,sector=sector,summary=summary,industry=industry,website=website,next_earnings_date=next_earnings_date)
        c_info.save()
        info_downloaded = True

    try:
        income_stmt, quarterly_income_stmt, balance_sheet, quarterly_balance_sheet, cashflow, quarterly_cashflow = get_financials(companieModel.ticker)
        
    except Exception as e:
        traceback.print_exc()
        print('error getting financials : ',e)
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
    ticker = models.CharField(max_length=10,unique=True)
    data_was_downloaded = models.BooleanField(default=False)
    created_at_date = models.DateTimeField(auto_now_add=True)
    image_link = models.CharField(max_length=250,default='')
    market_cap = models.FloatField(default=0)
    share_price = models.FloatField(default=0)
    one_day_variation = models.FloatField(default=0)
    
    def __str__(self):
        return self.name

    def save(self):
        super(Companie, self).save()
        if not self.data_was_downloaded and not CompanieInfo.objects.filter(ticker=self.ticker).exists():
            result = download_info(self)
            self.data_was_downloaded = result
            super(Companie, self).save()
        
class CompanieInfo(models.Model):
    name = models.OneToOneField(Companie,related_name='compagnie_info', on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100,unique=True)
    sector = models.CharField(max_length=100)
    summary = models.TextField()
    industry = models.CharField(max_length=100)
    website = models.CharField(max_length=250)
    last_updated_at = models.DateTimeField(auto_now_add=True)
    next_earnings_date = models.DateTimeField(null=True,blank=True,default=yesterday)

    def __str__(self):
        return self.name.name +' Infos'

    def delete(self):
        ticker = self.ticker
        
        company_balance_sheet = CompanieBalanceSheet.objects.filter(ticker=ticker)
        if company_balance_sheet.exists():
            company_balance_sheet[0].delete()
            
        company_income = CompanieIncomeStatement.objects.filter(ticker=ticker)
        if company_income.exists():
            company_income[0].delete()
        company_cash_flow = CompanieCashFlow.objects.filter(ticker=ticker)
        if company_cash_flow.exists():
            company_cash_flow[0].delete()
        super(CompanieInfo,self).delete()
        company = Companie.objects.get(ticker=ticker)
        #company = company[0]
        company.data_was_downloaded = False
        company.save()
        
class CompanieBalanceSheet(models.Model):
    name = models.OneToOneField(Companie, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100,unique=True)
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
        if not self.full_annual_balance_sheet.empty:
            self.full_num_col = self.full_annual_balance_sheet.shape[1]
            self.full_num_row = self.full_annual_balance_sheet.shape[0]
            self.light_num_col = self.light_annual_balance_sheet.shape[1]
            self.light_num_row = self.light_annual_balance_sheet.shape[0]
        super(CompanieBalanceSheet, self).save()
    
    def __str__(self):
        return self.name.name +' Balance Sheet'


class CompanieIncomeStatement(models.Model):
    name = models.OneToOneField(Companie, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100,unique=True)
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
        
        if not self.full_annual_income_statement.empty:
            self.full_num_col = self.full_annual_income_statement.shape[1]
            self.full_num_row = self.full_annual_income_statement.shape[0]
            self.light_num_col = self.light_annual_income_statement.shape[1]
            self.light_num_row = self.light_annual_income_statement.shape[0]
        super(CompanieIncomeStatement, self).save()
    def __str__(self):
        return self.name.name+ ' Income Statement'
class CompanieCashFlow(models.Model):
    name = models.OneToOneField(Companie, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100,unique=True)
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
        if not self.full_annual_cash_flow.empty:
            self.full_num_col = self.full_annual_cash_flow.shape[1]
            self.full_num_row = self.full_annual_cash_flow.shape[0]
            self.light_num_col = self.light_annual_cash_flow.shape[1]
            self.light_num_row = self.light_annual_cash_flow.shape[0]
        super(CompanieCashFlow, self).save()

    def __str__(self):
        return self.name.name+ ' Cash Flow'
    
    
    
class Currency(models.Model):
    name = models.CharField(max_length=100,unique=True)
    ticker = models.CharField(max_length=10,unique=True)
    last_updated_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField(default=0)
    
    def __str__(self):
        return self.name
    
def daily_update():
    #print('calling daily updates')
    last_update = DailyUpdateStatus.objects.all()[0]
    utc=pytz.UTC
    today = datetime.datetime.now()
    yesterday  = today - datetime.timedelta(days=1)
    if last_update.last_updated_at < utc.localize(yesterday):
        last_update.last_updated_at = today #we update directly to avoid concurent updates
        last_update.save()
        update_companies()
        
        
class DailyUpdateStatus(models.Model):
    name = models.CharField(max_length=100,unique=True)
    last_updated_at = models.DateTimeField(auto_now_add=True)
#daily_update()



def merge_df(new_df,old_df):
    old_columns  = list(old_df.columns)
    new_columns  = list(new_df.columns)
    for col in new_columns:
        if not col in old_columns:
           old_df[col] = new_df[col]
    return old_df
    

def update_financial_info(ticker,income_stmt,quarterly_income_stmt,balance_sheet,quarterly_balance_sheet, cashflow, quarterly_cashflow):
    try:
        old_income_stmt = CompanieIncomeStatement.objects.get(ticker=ticker)
        old_annual_income_statement = old_income_stmt.full_annual_income_statement
        old_quarterly_income_statement = old_income_stmt.full_quarterly_income_statement
        new_annual_income_statement = merge_df(income_stmt,old_annual_income_statement)
        new_quarterly_income_statement = merge_df(quarterly_income_stmt,old_quarterly_income_statement)
        new_light_annual_income_statement = shrink_income_stmt(new_annual_income_statement)
        new_light_quarterly_income_statement = shrink_income_stmt(new_quarterly_income_statement)
        old_income_stmt.full_annual_income_statement = new_annual_income_statement
        old_income_stmt.full_quarterly_income_statement = new_quarterly_income_statement
        old_income_stmt.light_annual_income_statement = new_light_annual_income_statement
        old_income_stmt.light_quarterly_income_statement = new_light_quarterly_income_statement
        old_income_stmt.save()
        
        old_balance_sheet = CompanieBalanceSheet.objects.get(ticker=ticker)
        old_annual_balance_sheet = old_balance_sheet.full_annual_balance_sheet
        old_quarterly_balance_sheet = old_balance_sheet.full_quarterly_balance_sheet
        new_annual_balance_sheet = merge_df(balance_sheet,old_annual_balance_sheet)
        new_quarterly_balance_sheet = merge_df(quarterly_balance_sheet,old_quarterly_balance_sheet)
        new_light_annual_balance_sheet = shrink_balance_sheet(new_annual_balance_sheet)
        new_light_quarterly_balance_sheet = shrink_balance_sheet(new_quarterly_balance_sheet)
        old_balance_sheet.full_annual_balance_sheet = new_annual_balance_sheet
        old_balance_sheet.full_quarterly_balance_sheet = new_quarterly_balance_sheet
        old_balance_sheet.light_annual_balance_sheet = new_light_annual_balance_sheet
        old_balance_sheet.light_quarterly_balance_sheet = new_light_quarterly_balance_sheet
        old_balance_sheet.save()
        
        old_cashflow = CompanieCashFlow.objects.get(ticker=ticker)
        old_annual_cashflow = old_cashflow.full_annual_cash_flow
        old_quarterly_cashflow = old_cashflow.full_quarterly_cash_flow
        new_annual_cashflow = merge_df(cashflow,old_annual_cashflow)
        new_quarterly_cashflow = merge_df(quarterly_cashflow,old_quarterly_cashflow)
        new_light_annual_cashflow = shrink_cashflow(new_annual_cashflow)
        new_light_quarterly_cashflow = shrink_cashflow(new_quarterly_cashflow)
        old_cashflow.full_annual_cash_flow = new_annual_cashflow
        old_cashflow.full_quarterly_cash_flow = new_quarterly_cashflow
        old_cashflow.light_annual_cash_flow = new_light_annual_cashflow
        old_cashflow.light_quarterly_cash_flow = new_light_quarterly_cashflow
        old_cashflow.save()
    except:
        return False
    else:
        return True
    
def reset_companies():
    companies = Companie.objects.all()
    
    for i,company in enumerate(companies):
        company_info = CompanieInfo.objects.filter(name=company)
        if company_info.exists():
         company_info.delete()
        
        income_stmt = CompanieIncomeStatement.objects.filter(name=company)
        if income_stmt.exists():
            income_stmt.delete()
        
        balance_sht = CompanieBalanceSheet.objects.filter(name=company)
        if balance_sht.exists():
            balance_sht.delete()
        
        cashflow = CompanieCashFlow.objects.filter(name=company)
        if cashflow.exists():
            cashflow.delete()
            
        company.data_was_downloaded = False
        company.save()
        
        
        
        
def updateAfterEarninigs():
    yesterday_ = datetime.date.today() - datetime.timedelta(days=1)
    companies = CompanieInfo.objects.filter(next_earnings_date__lt = yesterday_) #lower than yesterday give us more safety knowing the earnings are available
    
    if companies.exists():
        for company in companies:
            ticker = company.ticker
            #print(ticker)
            try:
                income_stmt, quarterly_income_stmt, balance_sheet, quarterly_balance_sheet, cashflow, quarterly_cashflow = get_financial_yahoo_info2(ticker)
            except Exception as e:
                print(e)
                successful_update = False
            else:
                successful_update = update_financial_info(ticker,income_stmt,quarterly_income_stmt,balance_sheet,quarterly_balance_sheet, cashflow, quarterly_cashflow)
            if successful_update:
                company_info = CompanieInfo.objects.get(ticker=ticker)
                #print(company_info)
                try:
                    next_earning = get_next_earnings_date(ticker)
                except Exception as e:
                    print(e)
                    next_earning = yesterday_
                #print(next_earning)
                company_info.next_earnings_date = next_earning
                company_info.save()

#update_companies()



        

  
        