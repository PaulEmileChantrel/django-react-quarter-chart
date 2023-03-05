
from django.test import TestCase,Client

# Create your tests here.
from django.urls import reverse
from django.shortcuts import render

from django.http import JsonResponse
from unittest.mock import patch
from .formatMktCap import formatMktCap
from api.models import Companie
class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_react(self):
        response = self.client.get(reverse('frontend-companielist'))
        #print(response.content.decode())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id=\'app\'>')
        self.assertContains(response, '<title>Search a Chart</title>')
        self.assertContains(response, '<script src="/static/frontend/main.js"></script>')

import json

class FrontendTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = Companie(name='Apple',ticker='AAPL',data_was_downloaded=True,market_cap=1000,created_at_date='2023-03-05T20:36:32.420760Z')
        self.company.save()
        
    def test_fetch_companies_list(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)
        companies_list = json.loads(response.content)
        self.assertTrue(len(companies_list)==1)
        # check if the data is in the expected format and contains the expected fields

    def test_filter_companies(self):
        response = self.client.get('/api/filterCompany/?name=A')

        self.assertEqual(response.status_code, 200)
        filtered_list = json.loads(response.content)
        self.assertTrue(len(filtered_list)==1)
        # check if the filtered list contains only the expected items

    def test_fetch_earnings_week(self):
        response = self.client.get('/api/next-earnings')
        self.assertEqual(response.status_code, 200)
        earnings_week = json.loads(response.content)
        self.assertTrue(len(earnings_week)==1)
        # check if the data is in the expected format and contains the expected fields
        
        

