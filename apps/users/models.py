from django.db import models
from django.conf import settings
from common import constants
from apps.stocks.models import Stock
from common.managers import ActiveObjectsManager
# Create your models here.

class Profile(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(null=True, max_length=30)
    address = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    active_objects = ActiveObjectsManager()
    
    def __str__(self):
        return f'Profile of {self.user.username}'
    
    class Meta: 
        ordering = ['-created_at']
        
        indexes = [
            models.Index(fields=['-created_at', 'is_active'])
        ]
    

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=20, choices=constants.CURRENCY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Account for {self.user.username}'
    
    class Meta: 
        ordering = ['-created_at']
        
        indexes = [
            models.Index(fields=['-created_at', 'balance', 'currency'])
        ]
    
class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_watchlist')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stock_watchlist')
    alert_price = models.DecimalField(max_digits=15, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Watchlist for {self.stock.company_name}'
    
    
    class Meta: 
        ordering = ['-created_at']
        
        indexes = [
            models.Index(fields=['-created_at', 'alert_price'])
        ]