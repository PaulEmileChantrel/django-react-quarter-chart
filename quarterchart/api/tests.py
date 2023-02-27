from django.test import TestCase,Client

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Companie,CompanieInfo,CompanieIncomeStatement,CompanieBalanceSheet,CompanieCashFlow
from .serializers import CompanieSerializer,CompanieFullInfoSerializer, CompanieInfoSerializer,NextEarningsSerializer,CompanieIncomeSerializer
from django.db.models import Q

class CompanieViewTestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        c1 = Companie(
            name='Test Company 1',
            ticker = 'T1',
            data_was_downloaded = True,
            market_cap=1000000,
        )
        c1.save()
        c2 = Companie(
            name='Test Company 2',
            ticker = 'T2',
            data_was_downloaded = True,
            market_cap=2000000,
        )
        c2.save()
        c3 = Companie(
            name='Test Company 3',
            ticker = 'T3',
            data_was_downloaded = True,
            market_cap=3000000,
        )
        c3.save()

    def test_get_companies(self):
        response = self.client.get(reverse('companielist'))
        companies = Companie.objects.filter(~Q(market_cap=0)).order_by('-market_cap')
        serializer = CompanieSerializer(companies, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
from rest_framework.test import APIClient
class FilterCompanieViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        c1 = Companie(
            name='Apple Inc.',
            ticker='AAPL',
            data_was_downloaded = True,
            market_cap=200000000000
        )
        c1.save()
        c2 = Companie(
            name='Microsoft Corp.',
            ticker='MSFT',
            data_was_downloaded = True,
            market_cap=150000000000
        )
        c2.save()
        c3 = Companie(
            name='Amazon.com Inc.',
            ticker='AMZN',
            data_was_downloaded = True,
            market_cap=100000000000
        )
        c3.save()

    def test_filter_companies_by_name_or_ticker(self):
        url = reverse('filter-companies')
        response = self.client.get(url, {'name': 'apple'})
        companies = Companie.objects.filter((Q(name__icontains='apple') | Q(ticker__icontains='apple')) & ~Q(market_cap=0)).order_by('-market_cap')
        serializer = CompanieSerializer(companies, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data, serializer.data)
        response = self.client.get(url, {'name': 'm'})
        self.assertEqual(len(response.data), 2)
        response = self.client.get(url, {'name': 'a'})
        self.assertEqual(len(response.data), 2)
        
class GetCompanieInfoTestCase(APITestCase):
    def setUp(self):
        self.apple = Companie(
            name='Apple Inc.',
            ticker='AAPL',
            data_was_downloaded = True,
            market_cap=200000000000
        )
        self.apple.save()
        self.apple_info = CompanieInfo(
            name=self.apple,
            summary='Apple is a multinational technology company.'
        )
        self.apple_info.save()

    def test_get_company_info_by_ticker(self):
        url = reverse('get-companie-info')
        response = self.client.get(url, {'ticker': 'AAPL'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Apple Inc.')
        self.assertEqual(response.data['summary'], 'Apple is a multinational technology company.')
        self.assertEqual(response.data['market_cap'], 200000000000)

    def test_get_company_info_with_invalid_ticker(self):
        url = reverse('get-companie-info')
        response = self.client.get(url, {'ticker': 'INVALID'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'Ticker Not Found': 'Invalid Request'})

    def test_get_company_info_with_missing_ticker(self):
        url = reverse('get-companie-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'Bad Request': 'ticker parameter not found in request'})
        
        
import unittest
from unittest.mock import patch,MagicMock
from .get_data.get_yahoo_info import get_mkt_cap


class TestGetMktCap(unittest.TestCase):
   
   
    @patch('api.get_data.get_yahoo_info.yf.Ticker')
    def test_get_mkt_cap(self, mock_ticker):
        mock_info = {'market_cap': 1000000000}
        mock_stock = MagicMock()
        
        mock_stock.fast_info = mock_info
        mock_ticker.return_value = mock_stock
        ticker = 'AAPL'

        market_cap = get_mkt_cap(ticker)
        mock_ticker.assert_called_once_with(ticker)
        
        self.assertEqual(market_cap, mock_info['market_cap'])
        
        
# class CreateCompanieViewTestCase(APITestCase):
#     url = reverse('create_companie')

#     def test_create_companie_successfully(self):
#         data = {'name': 'Test Company', 'ticker': 'TEST'}
#         response = self.client.post(self.url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Companie.objects.count(), 1)
#         self.assertEqual(Companie.objects.get().name, 'Test Company')
#         self.assertEqual(Companie.objects.get().ticker, 'TEST')

#     def test_create_companie_already_exists(self):
#         # Create a test company
#         c1 = Companie(name='Test Company', ticker='TEST',data_was_downloaded=True)
#         c1.save()
#         data = {'name': 'Test Company', 'ticker': 'TEST'}
#         response = self.client.post(self.url, data, format='json')
#         print(response.content.decode('utf-8'))
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Companie.objects.count(), 1)


from django.contrib.auth.models import User
class CreateCompanieViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            'name': 'Test Company',
            'ticker': 'TST'
        }
        self.invalid_payload = {
            'name': '',
            'ticker': ''
        }

    def test_create_valid_companie(self):
        response = self.client.post(
            reverse('create_companie'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.valid_payload['name'])
        self.assertEqual(response.data['ticker'], self.valid_payload['ticker'])

    def test_create_invalid_companie(self):
        response = self.client.post(
            reverse('create_companie'),
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
from datetime import datetime, timedelta   


class NextEarningsViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.today = datetime.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.yesyesterday = self.today - timedelta(days=2)
        self.c1 = Companie(name='Company 1',ticker='TK1',data_was_downloaded=True)
        self.c1.save()
        self.c2 = Companie(name='Company 2',ticker='TK2',data_was_downloaded=True)
        self.c2.save()
        self.company1 = CompanieInfo(
            name=self.c1,
            ticker = self.c1.ticker,
            next_earnings_date=self.tomorrow,
        )
        self.company1.save()
        
        self.company2 = CompanieInfo(
            name=self.c2,
            ticker = self.c2.ticker,
            next_earnings_date=self.yesyesterday,
        )
        self.company2.save()

    def test_get_next_earnings(self):
        response = self.client.get('/api/next-earnings')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        expected_data = NextEarningsSerializer(self.company1).data
        self.assertEqual(response.data[0], expected_data)
        
class UpdateSessionTimePeriodeTestCase(APITestCase):
    
    def setUp(self):
        self.url = reverse('update_session_time_periode')
        self.data = {'time_periode': 'quarter'}

    @patch('django.contrib.sessions.backends.db.SessionStore.exists', return_value=False)
    def test_patch_creates_session(self, mock_exists):
        self.session_key = self.client.session.session_key
        
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(mock_exists.called)
        self.new_session_key = self.client.session.session_key
        self.assertTrue(self.new_session_key!= self.session_key)
    
    def test_patch_sets_session_variable_to_quarter(self):
        self.client.session.create()
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.session['time_periode'], 'quarter')
    
    def test_patch_sets_session_variable_to_annual(self):
        self.client.session.create()
        self.data['time_periode'] = 'annual'
        response = self.client.patch(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.session['time_periode'], 'annual')
        
        
from .views import CompanyOtherChartData
from rest_framework.test import APIRequestFactory
import pandas as pd

class CompanyFirstChartDataTestCase(APITestCase):
    def test_company_first_chart_data_without_ticker_in_db(self):
        url = reverse('company_first_chart_data')
        response = self.client.get(url, {'ticker': 'AAPL'})
        
        self.assertEqual(response.status_code, 404)
        self.assertTrue("Ticker Not Found" in response.data)
        
    def test_company_first_chart_data_without_ticker_in_request(self):
        url = reverse('company_first_chart_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Bad Request" in response.data)
       
        
    def test_company_first_chart_data_with_ticker_in_db(self):
        c1 = Companie(name='Apple',ticker='AAPL',data_was_downloaded=True) 
          
        c1.save()
        c1_income_statement = CompanieIncomeStatement(name=c1,ticker='AAPL',full_annual_income_statement=pd.DataFrame(),full_quarterly_income_statement=pd.DataFrame(),light_annual_income_statement=pd.DataFrame(),light_quarterly_income_statement=pd.DataFrame())
        c1_income_statement.save()       
        url = reverse('company_first_chart_data')
        response = self.client.get(url, {'ticker': 'AAPL'})
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue("quarter" in response.data)
        self.assertTrue('annual' in response.data)
        self.assertTrue('time_periode' in response.data)
        
from .views import df_to_array


class DfToArrayTestCase(TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            '2022-01-01 00:00:00': [100, 200, 300],
            '2022-04-01 00:00:00': [400, 500, 600],
            '2022-07-01 00:00:00': [700, 800, 900],
            '2022-10-01 00:00:00': [1000, 1100, 1200],
            'TTM': [1300, 1400, 1500]
        }, index=['Total Revenue', 'Gross Profit', 'Operating Income'])

    def test_df_to_array_quarterly(self):
        rows = ['Total Revenue', 'Gross Profit', 'Operating Income']
        timeframe = 'q'
        expected_output = [['Dates', 'Total Revenue', 'Gross Profit', 'Operating Income'], ('Q1, 2022', 100, 200, 300), ('Q2, 2022', 400, 500, 600), ('Q3, 2022', 700, 800, 900), ('Q4, 2022', 1000, 1100, 1200)]
        
        self.assertEqual(df_to_array(self.df, rows, timeframe), expected_output)

    def test_df_to_array_annual(self):
        rows = ['Total Revenue', 'Gross Profit', 'Operating Income']
        timeframe = 'a'
        expected_output = [['Dates', 'Total Revenue', 'Gross Profit', 'Operating Income'], ('2022', 100, 200, 300), ('2022', 400, 500, 600), ('2022', 700, 800, 900), ('2022', 1000, 1100, 1200), ('TTM', 1300, 1400, 1500)]
        
        self.assertEqual(df_to_array(self.df, rows, timeframe), expected_output)

    def test_df_to_array_missing_row(self):
        rows = ['Total Revenue', 'Net Income', 'Operating Income']
        timeframe = 'q'
        expected_output = [['Dates', 'Total Revenue', 'Operating Income'], ('Q1, 2022', 100, 300), ('Q2, 2022', 400, 600), ('Q3, 2022', 700, 900), ('Q4, 2022', 1000, 1200)]
        self.assertEqual(df_to_array(self.df, rows, timeframe), expected_output)
        
        
    def test_df_to_array_no_row(self):
        rows = ['Net Income']
        timeframe = 'q'
        expected_output = []
        self.assertEqual(df_to_array(self.df, rows, timeframe), expected_output)
        
        
class CompanyOtherChartDataTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = Client()
        self.ticker = 'AAPL'
        # create test data
        c1 = Companie(name='Apple',ticker='AAPL',data_was_downloaded=True) 
        c1.save()
        c1_income_statement = CompanieIncomeStatement(name=c1,ticker='AAPL',full_annual_income_statement=pd.DataFrame(),full_quarterly_income_statement=pd.DataFrame(),light_annual_income_statement=pd.DataFrame(),light_quarterly_income_statement=pd.DataFrame())
        c1_income_statement.save()
        c1_balance_sheet = CompanieBalanceSheet(name=c1,ticker='AAPL',full_annual_balance_sheet=pd.DataFrame(),full_quarterly_balance_sheet=pd.DataFrame(),light_annual_balance_sheet=pd.DataFrame(),light_quarterly_balance_sheet=pd.DataFrame())
        c1_balance_sheet.save() 
        c1_cash_flow = CompanieCashFlow(name=c1,ticker='AAPL',full_annual_cash_flow=pd.DataFrame(),full_quarterly_cash_flow=pd.DataFrame(),light_annual_cash_flow=pd.DataFrame(),light_quarterly_cash_flow=pd.DataFrame())
        c1_cash_flow.save()   
        
    def test_get_company_data(self):
        url = reverse('company_other_chart_data')
        #url = f'/api/company-data/?ticker={self.ticker}'
        request = self.factory.get(url, {'ticker': 'AAPL'})
        response = CompanyOtherChartData.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['quarter'], [[], [], [], [], [], [], [], [], []])
        self.assertEqual(response.data['annual'], [[], [], [], [], [], [], [], [], []])

    def test_get_company_data_with_invalid_ticker(self):
        
        url = reverse('company_other_chart_data')
        request = self.factory.get(url,{'ticker': 'invalid_ticker'})
        response = CompanyOtherChartData.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'Ticker Not Found': 'Invalid Request'})

    def test_get_company_data_with_missing_ticker_param(self):
        url = reverse('company_other_chart_data')
        request = self.factory.get(url)
        response = CompanyOtherChartData.as_view()(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'Bad Request': 'ticker parameter not found in request'})
        

class CompanieModelTest(TestCase):
    
    def setUp(self):
        self.company = Companie(name="Test Company", ticker="AAPL")
        #self.company.save()
    
    def test_str(self):
        self.assertEqual(str(self.company), "Test Company")
    
    def test_save(self):
        # Check that data_was_downloaded is False and no CompanieInfo exists
        self.assertFalse(self.company.data_was_downloaded)
        self.assertFalse(CompanieInfo.objects.filter(ticker=self.company.ticker).exists())
        
        # Call save method to download data
        self.company.save()
        
        # Check that data_was_downloaded is True and a CompanieInfo object exists
        self.assertTrue(self.company.data_was_downloaded)
        self.assertTrue(CompanieInfo.objects.filter(ticker=self.company.ticker).exists())
        
        # Call save method again to ensure that it doesn't redownload the data
        self.company.save()
        self.assertTrue(CompanieInfo.objects.filter(ticker=self.company.ticker).exists())
        
        self.assertTrue(CompanieIncomeStatement.objects.filter(ticker=self.company.ticker).exists())
        self.assertTrue(CompanieBalanceSheet.objects.filter(ticker=self.company.ticker).exists())
        self.assertTrue(CompanieCashFlow.objects.filter(ticker=self.company.ticker).exists())
        
from django.utils import timezone    
class CompanieInfoTestCase(TestCase):
    def setUp(self):
        self.company = Companie(name='Test Company', ticker='TEST',data_was_downloaded=True)
        self.company.save()
        self.today = timezone.now()
        self.yesterday = self.today - timezone.timedelta(days=1)

    def test_create_companie_info(self):
        companie_info = CompanieInfo(
            name=self.company,
            ticker='TEST',
            sector='Technology',
            summary='This is a test company in the technology sector',
            industry='Software',
            website='http://www.testcompany.com',
            last_updated_at=self.today,
            next_earnings_date=self.yesterday
        )
        companie_info.save()
        self.assertEqual(companie_info.__str__(), 'Test Company Infos')

    def test_delete_companie_info(self):
        companie_info = CompanieInfo(
            name=self.company,
            ticker='TEST',
            sector='Technology',
            summary='This is a test company in the technology sector',
            industry='Software',
            website='http://www.testcompany.com',
            last_updated_at=self.today,
            next_earnings_date=self.yesterday
        )
        companie_info.save()
        companie_info.delete()
        company = Companie.objects.get(ticker='TEST')
        self.assertFalse(company.data_was_downloaded)