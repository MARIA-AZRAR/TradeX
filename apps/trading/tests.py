
from decimal import Decimal
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.stocks.models import Stock
from apps.users.models import Account
from .models import Portfolio, Transaction

User = get_user_model()

class TransactionViewTest(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'user@test.com', 'testpass')
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'adminpass')
        self.stock = Stock.objects.create(company_name="Sample Stock", tick= "SAMPLE2", description= "This is a sample stock",
            current_price= 150.00,  volume= 1000, outstanding_shares= 500000, currency= "USD", stock_type= "TECH",
            list_date= "2024-02-13")
        
        self.transaction_url = reverse('make-transaction')
        self.transaction_list_url = reverse('transaction')
        

    def test_create_buy_transaction(self):
        """Test creating a buy transaction"""
        account = Account.objects.create(user=self.user, balance=5000.00, currency='USD')
        
        # Expected values after the transaction
        expected_sale_amount = float(150.00 * 10)  # price per share * quantity
        expected_new_balance = account.balance - expected_sale_amount
        expected_new_stock_volume = self.stock.volume - 10
        
        self.client.force_authenticate(user=self.user)
        data = {
            'stock_symbol': 'SAMPLE2',
            'quantity': 10,
            'transaction_type': 'buy'
        }
        response = self.client.post(self.transaction_url, data)
        self.assertEqual(response.status_code, 201)
        
        # Check if the correct amount has been credited to the account balance
        account.refresh_from_db()
        self.assertEqual(account.balance, expected_new_balance)

        # Check if the correct volume has been added back to the stock
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.volume, expected_new_stock_volume)
        
        

    def test_create_sell_transaction(self):
        """Test creating a sell transaction"""
        self.client.force_authenticate(user=self.user)
        Account.objects.create(user=self.user, balance=5000.00, currency='USD')
        Portfolio.objects.create(user=self.user, stock=self.stock, quantity=10, purchase_price=100.00)
        
        data = {
            'stock_symbol': 'SAMPLE2',
            'quantity': 5,
            'transaction_type': 'sell'
        }
        
        response = self.client.post(self.transaction_url, data)
        self.assertEqual(response.status_code, 201)

    def test_transaction_list(self):
        """Test listing transactions for the user"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.transaction_list_url)
        self.assertEqual(response.status_code, 200)

    def test_transaction_status_update_by_admin(self):
        """Test updating the status of a transaction by admin"""
        Portfolio.objects.create(user=self.user, stock=self.stock, quantity=15, purchase_price=100.00)
        
        transaction = Transaction.objects.create(
            user=self.user, stock=self.stock, quantity=10, price_at_transaction=150.00, 
            transaction_type='sell', status='pending'
        )
        account = Account.objects.create(user=self.user, balance=5000.00, currency='USD')
        
        # Expected values after the transaction
        expected_sale_amount = float(150.00 * 10)  # price per share * quantity
        expected_new_balance = account.balance + expected_sale_amount
        expected_new_stock_volume = self.stock.volume + 10
        
        transaction_status_url = reverse('transaction-update-status', kwargs={'pk': transaction.id})
        self.client.force_authenticate(user=self.admin)
        data = {'status': 'completed'}
        response = self.client.patch(transaction_status_url, data)
        
        self.assertEqual(response.status_code, 200)
        transaction.refresh_from_db()
        self.assertEqual(transaction.status, 'completed')

        # Check if the correct amount has been credited to the account balance
        account.refresh_from_db()
        self.assertEqual(account.balance, expected_new_balance)

        # Check if the correct volume has been added back to the stock
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.volume, expected_new_stock_volume)
        
    def test_transaction_status_update_fail(self):
        """Test failing to update a non-pending transaction"""
        transaction = Transaction.objects.create(
            user=self.user, stock=self.stock, quantity=10, price_at_transaction=150.00, 
            transaction_type='sell', status='completed'
        )
        
        Portfolio.objects.create(user=self.user, stock=self.stock, quantity=15, purchase_price=100.00)
        transaction_status_url = reverse('transaction-update-status', kwargs={'pk': transaction.id})
        
        self.client.force_authenticate(user=self.admin)
        data = {'status': 'completed'}
        response = self.client.patch(transaction_status_url, data)
        self.assertEqual(response.status_code, 400)
