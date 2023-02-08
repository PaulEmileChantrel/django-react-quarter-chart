from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from django.db.models import Q
from .serializers import CompanieSerializer,CreateCompanieSerializer,CompanieInfoSerializer,CompanieFullInfoSerializer
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

update_light_income_statement()