
from django.test import TestCase,Client

# Create your tests here.
from django.urls import reverse
from api.models import Companie,CompanieInfo
import datetime
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
        self.company = Companie(name='Apple',ticker='AAPL',data_was_downloaded=True,market_cap=1000)
        self.company.save()
        tomorrow = datetime.datetime.now()+datetime.timedelta(days=1)
        self.company_info = CompanieInfo(name = self.company, ticker ='AAPL',next_earnings_date = tomorrow)#long in the future
        self.company_info.save()
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
        print(earnings_week)
        self.assertTrue(len(earnings_week)==1)
        # check if the data is in the expected format and contains the expected fields
        
        

