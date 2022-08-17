import unittest
from django.test import TestCase, override_settings, Client
from .models import Transaction
from .forms import TransactionForm
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from http import HTTPStatus 
from bs4 import BeautifulSoup
from django.conf import settings 


class TransactionIndexViewTests(TestCase):
    fixtures = ["transactions.json"]
    
    def test_fixture(self):
        self.assertEqual(len(Transaction.objects.all()), 2)
    def test_url_setting(self):
        with self.settings(TRANSACTION_URL='trx'):
            # self.assertRaises(NoReverseMatch, reverse(settings.TRANSACTION_URL+':index'))
            self.assertRaises( reverse(settings.TRANSACTION_URL+':index'))
            response = self.client.get(
                reverse(settings.TRANSACTION_URL+':index')
            )
            self.assertEqual(response.status_code, 200)
    @override_settings(TRANSACTION_URL='trx')
    def test_url_setting_with_decorator(self):
        # self.assertRaises(NoReverseMatch ,reverse(settings.TRANSACTION_URL+':index'))
        response = self.client.get(
            reverse(settings.TRANSACTION_URL + ":index")
        )
        self.assertEqual(response.status_code, 200)
    def test_blank_form_submission(self):
        response = self.client.post(
            "/transaction/", data={}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Transaction.objects.all()), 2)
    def test_valid_form_submission(self):
        response = self.client.post(
            "/transaction/",
            data ={
                "product_code":"p123",
                "quantity":1,
                "price":89
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Transaction.objects.all()), 3)
        self.assertIn("POS", str(response.content)) #POS is the page title
        self.assertContains(response, "POS", 1) #unlike In test contains specify num of substring instance
    def test_count_of_transactions_in_report(self):
        response = self.client.get(reverse('report:index'))
        self.assertContains(response, "POS Report", 1)
        self.assertContains(response, "<li>", 2)
    def test_html(self):
        response = self.client.get(reverse('report:index'))
        soup = BeautifulSoup(str(response.content))
        li = soup.find_all('li')[0]
        #html assert ignore valuable content of html like textContent  while ignoring entity like classname id or spaces
        self.assertHTMLEqual(str(li), '<li     >Laptop_2_1000.0</li>')
        self.assertInHTML('<li>Laptop_2_1000.0</li>', str(response.content))