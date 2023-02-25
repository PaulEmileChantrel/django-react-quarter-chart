from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.db.models import Q
from .serializers import CompanieSerializer,CreateCompanieSerializer,CompanieInfoSerializer,CompanieFullInfoSerializer, CompanieIncomeSerializer,NextEarningsSerializer
from datetime import datetime,date,timedelta
from .get_data.get_yahoo_info import get_mkt_cap,get_share_price
# Create your views here.
class CompanieView(generics.ListAPIView):
    queryset = Companie.objects.filter(~Q(market_cap=0)).order_by('-market_cap')
    serializer_class = CompanieSerializer

class FilterCompanieView(generics.ListAPIView):
    serializer_class = CompanieSerializer

    def get_queryset(self):
        return Companie.objects.filter((Q(name__icontains=self.request.query_params['name'])|Q(ticker__icontains=self.request.query_params['name']))&~Q(market_cap=0)).order_by('-market_cap')
class GetCompanieInfo(APIView):
    serializer_class = CompanieFullInfoSerializer
    lookup_url_kwarg = 'ticker'

    def get(self, request, format = None):
        ticker = request.GET.get(self.lookup_url_kwarg)
        if ticker != None:
            companie = Companie.objects.filter(ticker=ticker)
            
            if len(companie) > 0:
                companie_info = CompanieInfo.objects.filter(name=companie[0])
                data = CompanieFullInfoSerializer(companie[0]).data
                data2 = CompanieInfoSerializer(companie_info[0]).data
                
                data.update(data2)
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Ticker Not Found' : 'Invalid Request'},status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request' : 'ticker parameter not found in request'},status=status.HTTP_400_BAD_REQUEST)
class CreateCompanieView(APIView):
    serializer_class = CreateCompanieSerializer

    def post(self, request,format = None):
        #does the user has a session?
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        # is the data sent valid?
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() and self.request.user.is_staff: #check if the user is admin
            #if the company exist, the serializer will not be valid
            name = serializer.data.get('name')
            ticker = serializer.data.get('ticker')
            
            company = Companie(name=name,ticker=ticker)
            company.save()
            return Response(CompanieSerializer(company).data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def df_to_array(df,rows,timeframe):
    #df = df[df.columns[::-1]]
    df.fillna(0,inplace=True)
    head = ['Dates']+rows
    if timeframe == 'a':
        dates = list(df.columns)
        
        dates = [str(datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S').year) if date!='TTM' else 'TTM' for date in dates ]
    else:
        dates = list(df.columns)
        dates = [f"Q{str((datetime.strptime(str(date),'%Y-%m-%d %H:%M:%S').month)//4+1)}, {str(datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S').year)}" for date in dates if date!='TTM']
    row_list = [dates]
    

    for row in rows:
        try:
            row_list.append(list(df.loc[row]))
        except:
            head.remove(row)
    
    if len(head)==1:
        return []
    serialize_data = [head]+list(zip(*row_list))
    
    return serialize_data
    
               

class CompanyFirstChartData(APIView):
    serializer_class = CompanieIncomeSerializer
    lookup_url_kwarg_ticker = 'ticker'
    

    def get(self, request, format = None):
    
        ticker = request.GET.get(self.lookup_url_kwarg_ticker)
        
        #does the user has a session?
        if not self.request.session.exists(self.request.session.session_key) or not self.request.session.exists('time_periode'):
            self.request.session.create()
            time_periode = "quarter"
            self.request.session['time_periode'] = 'quarter'
        else:
            time_periode = self.request.session['time_periode']

        
        if ticker != None:
            companie = CompanieIncomeStatement.objects.filter(ticker=ticker)
            #save session user timeframe
            if len(companie) > 0:
                
                data_q = companie[0].light_quarterly_income_statement
                
                data_a = companie[0].light_annual_income_statement
                print(data_a)
                serialize_data_q = df_to_array(data_q,['Total Revenue','Gross Profit','Operating Income'],'q')
                serialize_data_a = df_to_array(data_a,['Total Revenue','Gross Profit','Operating Income'],'a')
                
                data = {'quarter': serialize_data_q,'annual': serialize_data_a,'time_periode':time_periode}
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Ticker Not Found' : 'Invalid Request'},status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request' : 'ticker parameter not found in request'},status=status.HTTP_400_BAD_REQUEST)

class CompanyOtherChartData(APIView):
    lookup_url_kwarg_ticker = 'ticker'

    def get(self, request, format = None):
        ticker = request.GET.get(self.lookup_url_kwarg_ticker)
        if ticker != None:
            companie_inc_stmt = CompanieIncomeStatement.objects.filter(ticker=ticker)
            companie_balance = CompanieBalanceSheet.objects.filter(ticker=ticker)
            companie_cash_flow = CompanieCashFlow.objects.filter(ticker=ticker)
            #save session user timeframe
            if companie_inc_stmt.exists() and companie_balance.exists() and companie_cash_flow.exists():
                
                inc_stmt_q = companie_inc_stmt[0].light_quarterly_income_statement
                inc_stmt_a = companie_inc_stmt[0].light_annual_income_statement

                bal_sht_q = companie_balance[0].light_quarterly_balance_sheet
                bal_sht_a = companie_balance[0].light_annual_balance_sheet

                cf_q = companie_cash_flow[0].light_quarterly_cash_flow
                cf_a = companie_cash_flow[0].light_annual_cash_flow
                
                #income statement
                chart1_q = df_to_array(inc_stmt_q,['Net Income'],'q')
                chart1_a = df_to_array(inc_stmt_a,['Net Income'],'a')

                chart2_q = df_to_array(inc_stmt_q,['Operating Expense'],'q')
                chart2_a = df_to_array(inc_stmt_a,['Operating Expense'],'a')
                
                #balance sheet
                chart3_q = df_to_array(bal_sht_q,['Current Assets','Total Non Current Assets'],'q')
                chart3_a = df_to_array(bal_sht_a,['Current Assets','Total Non Current Assets'],'a')

                chart4_q = df_to_array(bal_sht_q,['Total Liabilities Net Minority Interest', 'Stockholders Equity'],'q')
                chart4_a = df_to_array(bal_sht_a,['Total Liabilities Net Minority Interest', 'Stockholders Equity'],'a')

                chart5_q = df_to_array(bal_sht_q,['Total Debt'],'q')
                chart5_a = df_to_array(bal_sht_a,['Total Debt'],'a')

                #cash flow
                chart6_q = df_to_array(cf_q,['Investing Cash Flow', 'Operating Cash Flow','Free Cash Flow','Financing Cash Flow'],'q')
                chart6_a = df_to_array(cf_a,['Investing Cash Flow', 'Operating Cash Flow','Free Cash Flow','Financing Cash Flow'],'a')
                

                chart7_q = df_to_array(cf_q,['End Cash Position'],'q')
                chart7_a = df_to_array(cf_a,['End Cash Position'],'a')
                
                #others (ebita and eps)
                chart8_q = df_to_array(inc_stmt_q,['Normalized EBITDA'],'q')
                chart8_a = df_to_array(inc_stmt_a,['Normalized EBITDA'],'a')

                chart9_q = df_to_array(inc_stmt_q,['Basic EPS'],'q')
                chart9_a = df_to_array(inc_stmt_a,['Basic EPS'],'a')


                serialize_data_q = [chart1_q,chart2_q,chart3_q,chart4_q,chart5_q,chart6_q,chart7_q,chart8_q,chart9_q]
                serialize_data_a = [chart1_a,chart2_a,chart3_a,chart4_a,chart5_a,chart6_a,chart7_a,chart8_a,chart9_a]


                data = {'quarter': serialize_data_q,'annual': serialize_data_a}
                
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Ticker Not Found' : 'Invalid Request'},status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request' : 'ticker parameter not found in request'},status=status.HTTP_400_BAD_REQUEST)
class UpdateSessionTimePeriode(APIView):
    serializer_class = CompanieIncomeSerializer
    
    def patch(self, request, format = None):
        
        
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        time_periode = self.request.data.get('time_periode')
        if time_periode == 'quarter': # making sure that the parameter is either quarter or annual
            self.request.session['time_periode'] = time_periode
        else:
            self.request.session['time_periode'] = 'annual'
        return Response(status=status.HTTP_200_OK)
        

class NextEarningsView(generics.ListAPIView):
    serializer_class = NextEarningsSerializer
    yesterday = date.today() - timedelta(days=1)
    queryset = CompanieInfo.objects.filter(next_earnings_date__gt = yesterday).order_by('next_earnings_date')
    


#updateAfterEarninigs() 