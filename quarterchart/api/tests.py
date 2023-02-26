from django.test import TestCase,Client

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Companie,CompanieInfo
from .serializers import CompanieSerializer,CompanieFullInfoSerializer, CompanieInfoSerializer,NextEarningsSerializer
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
        print(self.client.session.session_key)
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