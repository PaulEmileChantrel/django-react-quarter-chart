
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
    rows = set(['Revenue','Gross Profit','Operating Income','Operating Expenses','Net Income','EPS','EBITDA','Research And Development Expenses','Selling General And Administrative Expenses','Selling And Marketing Expenses','General And Administrative Expenses','Gross Profit Ratio','Operating Income Ratio','Other Expenses'])
    rows = list(rows.intersection(set(df.index)))
    df = df.loc[rows]
    #print(df)
    
    if 'Gross Profit Ratio' in df.index  :
        df.loc['Gross Margin'] = df.loc['Gross Profit Ratio']*100
    if 'Operating Income Ratio' in df.index :
        df.loc['Operative Margin'] = df.loc['Operating Income Ratio'] *100
    return df

def shrink_balance_sheet(df):
    rows = set(['Total Assets','Total Current Assets','Total Non Current Assets',"Total Debt",'Total Liabilities','Total Stockholders Equity'])
    rows = list(rows.intersection(set(df.index)))
    return df.loc[rows]
    
    

def shrink_cashflow(df):
    rows = set(['Operating Cash Flow','Capital Expenditure','Free Cash Flow','Cash At End Of Period'])
    rows = list(rows.intersection(set(df.index)))
    return df.loc[rows]

def yesterday():
    return datetime.date.today() - datetime.timedelta(days=1)



