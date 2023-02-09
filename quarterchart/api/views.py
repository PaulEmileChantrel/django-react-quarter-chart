from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.db.models import Q
from .serializers import CompanieSerializer,CreateCompanieSerializer,CompanieInfoSerializer,CompanieFullInfoSerializer, CompanieIncomeSerializer
from .get_data.get_yahoo_info import get_mkt_cap
# Create your views here.
class CompanieView(generics.ListAPIView):
    queryset = Companie.objects.all().order_by('-market_cap')

    serializer_class = CompanieSerializer

class FilterCompanieView(generics.ListAPIView):
    serializer_class = CompanieSerializer

    def get_queryset(self):
        return Companie.objects.filter(Q(name__icontains=self.request.query_params['name'])|Q(ticker__icontains=self.request.query_params['name']))
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
        if serializer.is_valid():
            name = serializer.data.get('name')
            ticker = serializer.data.get('ticker')

            #check if company already exists
            queryset = Companie.objects.filter(ticker=ticker)
            if queryset.exists():
                company = queryset.first()
                # the company already exists
                return Response(CompanieSerializer(company).data,status=status.HTTP_208_ALREADY_REPORTED)
            else:
                company = Companie(name=name,ticker=ticker)
                company.save()
                return Response(CompanieSerializer(company).data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CompanyChartData(APIView):
    serializer_class = CompanieIncomeSerializer
    lookup_url_kwarg_ticker = 'ticker'
    lookup_url_kwarg_time = 'time'

    def get(self, request, format = None):
    
        ticker = request.GET.get(self.lookup_url_kwarg_ticker)
        time = request.GET.get(self.lookup_url_kwarg_time)
        if ticker != None and time!= None:
            companie = CompanieIncomeStatement.objects.filter(ticker=ticker)
            
            
            if len(companie) > 0:
                if time =='quarter':
                    data = companie[0].light_quarterly_income_statement
                else:
                    data = companie[0].light_annual_income_statement
                data = data[data.columns[::-1]]
                dates = list(data.columns)
                total_revenue = list(data.loc['Total Revenue'])
                gross_profit = list(data.loc['Gross Profit'])
                net_income = list(data.loc['Net Income'])
                
                # total_revenue = [str(x) for x in total_revenue]
                # gross_profit = [str(x) for x in gross_profit]
                # net_income = [str(x) for x in net_income]
                serialize_data = [['Dates','Total Revenue','Gross Profit','Net Income']]+list(zip(dates,total_revenue,gross_profit,net_income))
                
                return Response(serialize_data, status=status.HTTP_200_OK)
            return Response({'Ticker Not Found' : 'Invalid Request'},status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad Request' : 'ticker parameter not found in request'},status=status.HTTP_400_BAD_REQUEST)




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
        income_stmt = CompanieIncomeStatement.objects.filter(name=cpn).first()
        a_inc_stmt = income_stmt.full_annual_income_statement
        q_inc_stmt = income_stmt.full_quarterly_income_statement
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

def update_all():

    update_light_cash_flow()
    update_light_balance_sheet()
    update_light_income_statement()
    update_all_mkt_cap()
#update_all_mkt_cap()
#update_all() 