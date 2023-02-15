import pandas as pd
from .models import Companie

def load_companies():
   companies_df = pd.read_csv('topMarketCap.csv')
   companies_df[:10]
   companies_names = companies_df['name'].tolist()
   companies_ticker = companies_df['ticker'].tolist()
   for (name, ticker) in zip(companies_names, companies_ticker):
      company = Companie.objects.filter(name=name)
      if not company.exists():
         company = Companie(name=name, ticker=ticker)
         company.save()

if __name__ == '__main__':
   load_companies()