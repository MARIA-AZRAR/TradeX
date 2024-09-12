from django.db import models
from django.conf import settings
from apps.stocks.models import Stock
# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_portfolio')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stock_portfolio')
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s portfolio - {self.stock.company_name}"
    
    class Meta: 
        ordering = ['-created_at']
        
        indexes = [
            models.Index(fields=['-created_at', 'purchase_price', 'quantity'])
        ]
    
    @property
    def current_value(self):
        """ Returns current value of stocks """
        return self.stock.current_price * self.quantity
    
    @property
    def profit_loss(self):
        """ Calculate profit or loss for the stock in the portfolio """
        return (self.stock.current_price - self.purchase_price) * self.quantity
    
class Transaction(models.Model):
    class TransactionTypes(models.TextChoices):
        BUY = 'buy', 'Buy'
        SELL = 'sell', 'Sell'
    
    class StatusTypes(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'
    
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_transaction')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stock_transaction')
    quantity = models.IntegerField()
    price_at_transaction = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(max_length=4, choices=TransactionTypes.choices)
    status = models.CharField(max_length=10, choices=StatusTypes.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.transaction_type} : {self.quantity} shares of {self.stock.company_name} by {self.user.username}"
    
    
    class Meta: 
        ordering = ['-created_at']
        
        indexes = [
            models.Index(fields=['transaction_type', '-created_at', 'quantity'])
        ]
        
    @property
    def transaction_total(self):
        """Calculate the total amount of the transaction"""
        return self.quantity * self.price_at_transaction

    @property
    def is_successful(self):
        """Check if the transaction was completed successfully"""
        return self.status == self.StatusTypes.COMPLETED