from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Stock, PriceChangeLog


class StockViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'user@gmail.com', 'test')
        
        self.stock = Stock.objects.create(company_name="Sample Stock", tick= "SAMPLE2", description= "This is a sample stock",
            current_price= 100.5,  volume= 50000, outstanding_shares= 500000, currency= "GBP", stock_type= "TECH",
            list_date= "2024-02-13")
        
        # Temporarily remove True` for testing
        PriceChangeLog._meta.get_field('created_at').auto_now_add = False
        
        # Create price change log
        self.price_log_old1 = PriceChangeLog(
            stock=self.stock,
            old_price=150.0,
            new_price=155.5
        )
        self.price_log_old1.created_at = timezone.now() - timezone.timedelta(days=3)
        self.price_log_old1.save()
        
        self.price_log_old2 = PriceChangeLog(
            stock=self.stock,
            old_price=140.0,
            new_price=150.0
        )
        
        self.price_log_old2.created_at = timezone.now() - timezone.timedelta(days=2)
        self.price_log_old2.save()


        self.stock_list_url = reverse('stocks-list')
    
    def test_list_stocks_authenticated(self):
        """Test authenticated users can list stocks""" 
        self.client.force_login(user=self.user)
        response = self.client.get(self.stock_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_stocks_unauthenticated(self):
        """Test unauthenticated users cannot list stocks"""
        response = self.client.get(self.stock_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_previous_close_price(self):
        """Test fetching the previous close price"""
        # Previous close price should be the new_price of the last log from the previous day
        self.assertEqual(self.stock.previous_close_price, 150.0)
    
    def test_previous_close_price_no_previous_logs(self):
        """Test previous close price when there are no previous logs"""
        # Clear all logs and check fallback
        PriceChangeLog.objects.all().delete()
        self.assertEqual(self.stock.previous_close_price, self.stock.current_price) 