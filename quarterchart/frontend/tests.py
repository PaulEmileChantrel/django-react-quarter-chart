
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

