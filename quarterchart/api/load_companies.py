import pandas as pd
from .models import Companie

def load_companies():
   companies_df = pd.read_csv('topMarketCap.csv')
   companies_df[:100]
   companies_names = companies_df['name'].tolist()
   companies_ticker = companies_df['ticker'].tolist()
   for (name, ticker) in zip(companies_names, companies_ticker):
      company = Companie.objects.filter(name=name)
      if not company.exists():
         print(f'saving {ticker}')
         company = Companie(name=name, ticker=ticker)
         company.save()
         print(f'{ticker} saved successfully')

if __name__ == '__main__':
   load_companies()