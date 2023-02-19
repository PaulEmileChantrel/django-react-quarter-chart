from django.test import TestCase,Client

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Companie
from .serializers import CompanieSerializer
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