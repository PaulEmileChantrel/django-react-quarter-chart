
from config import API_KEY
import json,requests,datetime

def api_call(currency):
   
   url = f"https://api.apilayer.com/exchangerates_data/convert?to=USD&from={currency}&amount=1"

   payload = {}
   headers= {
   "apikey": API_KEY,
   }

   response = requests.request("GET", url, headers=headers, data = payload)

   
   result = response.text
   result = json.loads(result)
   
   result = result['info']['rate']
   return result

def shrink_income_stmt(df):
    rows = set(['Total Revenue','Gross Profit','Operating Income','Operating Expense','Net Income','Basic EPS','Normalized EBITDA'])
    rows = list(rows.intersection(set(df.index)))
    return df.loc[rows]

def shrink_balance_sheet(df):
    rows = set(['Total Assets','Current Assets','Total Non Current Assets',"Total Debt",'Total Liabilities Net Minority Interest','Stockholders Equity'])
    rows = list(rows.intersection(set(df.index)))
    return df.loc[rows]
    
    

def shrink_cashflow(df):
    rows = set(['Operating Cash Flow','Investing Cash Flow','Financing Cash Flow','Beginning Cash Position','End Cash Position','Free Cash Flow'])
    rows = list(rows.intersection(set(df.index)))
    return df.loc[rows]

def yesterday():
    return datetime.date.today() - datetime.timedelta(days=1)



