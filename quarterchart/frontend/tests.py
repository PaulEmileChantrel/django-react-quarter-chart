from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.shortcuts import render

from django.http import JsonResponse
from unittest.mock import patch
from .formatMktCap import formatMktCap
from api.models import Companie
class CompanyTestCase(TestCase):
    def setUp(self):
        # Create a dummy company object for testing
        self.company = {
            'name': 'Test Company',
            'ticker': 'TST',
            'market_cap': 1000000000,
            'share_price': 10.0,
            'one_day_variation': 1.23,
        }
        c1 = Companie(
            name='Test Company',
            ticker = 'TST',
            data_was_downloaded = True,
            market_cap =1000000,
            share_price = 10.0,
            one_day_variation = 1.23,
        )
        c1.save()
        
    def test_company_render(self):
        # Test that the Company component renders correctly
        
        # Get the URL of the Company component with the dummy company object as a prop
        url = reverse('frontend-companielist')
       
        
        # Use the Django test client to make a GET request to the URL
        response = self.client.get(url)
        print(response.content.decode())
        
        # Render the response content as a Django template and extract the rendered HTML
        rendered_html = render(response.request, 'index.html', {'content': response.content.decode()}).content.decode()
        
        # Assert that the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Assert that the rendered HTML contains the company name and ticker
        self.assertContains(rendered_html, self.company['name'])
        self.assertContains(rendered_html, self.company['ticker'])
        
        # Assert that the rendered HTML contains the formatted market cap and share price
        self.assertContains(response, '$ ' + formatMktCap(self.company['market_cap']))
        self.assertContains(response, '$ ' + str(round(self.company['share_price'],2)))
        
        # Assert that the rendered HTML contains the correct variation icon and value
        if self.company['one_day_variation'] == 0:
            self.assertContains(response, '<BiCaretRightCircle')
        elif self.company['one_day_variation'] > 0:
            self.assertContains(response, '<BiCaretUpCircle')
        else:
            self.assertContains(response, '<BiCaretDownCircle')
        self.assertContains(response, str(self.company['one_day_variation']) + ' %')

    