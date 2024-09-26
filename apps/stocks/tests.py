from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Stock


class StockViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'user@gmail.com', 'test')
        
        Stock.objects.create(company_name="Sample Stock", tick= "SAMPLE2", description= "This is a sample stock",
            current_price= 100.5,  volume= 50000, outstanding_shares= 500000, currency= "GBP", stock_type= "TECH",
            list_date= "2024-02-13")
        self.stock_list_url = reverse('stocks-list')
    
    def test_list_stocks_authenticated(self):
        # Ensure authenticated users can list stocks
        self.client.force_login(user=self.user)
        response = self.client.get(self.stock_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_stocks_unauthenticated(self):
        # Ensure unauthenticated users cannot list stocks
        response = self.client.get(self.stock_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)