from django.db import models
from datetime import timedelta
from common import constants
from django.utils import timezone

from common.managers import ActiveObjectsManager

# Create your models here.

class Stock(models.Model):
    class StockTypes(models.TextChoices):
        TECHNOLOGY = 'TECH', 'Technology'
        HEALTHCARE = 'HEAL', 'Healthcare'
        FINANCE = 'FIN', 'Finance'
        ENERGY = 'ENER', 'Energy'
        CONSUMER_GOODS = 'CG', 'Consumer Goods'
        UTILITIES = 'UTIL', 'Utilities'
        MATERIALS = 'MATE', 'Materials'
        INDUSTRIALS = 'IND', 'Industrials'
        TELECOMMUNICATIONS = 'TEL', 'Telecommunications'
    
    company_name = models.CharField(max_length=250) 
    tick = models.CharField(max_length=50, null=False, unique=True) 
    description = models.TextField()
    volume = models.BigIntegerField()
    current_price = models.DecimalField(max_digits=15, decimal_places=2)
    outstanding_shares = models.BigIntegerField()
    list_date = models.DateField()
    stock_type = models.CharField(max_length=20, choices=StockTypes.choices)
    is_active = models.BooleanField(default=True)
    currency = models.CharField(max_length=20, choices=constants.CURRENCY_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = models.Manager()
    active_objects = ActiveObjectsManager()
    
    class Meta: 
        ordering = ['-tick']
        
        indexes = [
            models.Index(fields=['tick', '-list_date', 'currency'])
        ]
    
    def __str__(self):
        return f'{self.company_name} at the price of {self.current_price} {self.currency} per share'
    
    @property
    def market_cap(self):
        return self.outstanding_shares * self.current_price
    
    @property
    def price_change(self):
        """Returns the price change from the most recent log entry."""
        last_log = self.price_logs.first()
        if last_log:
            return last_log.new_price - last_log.old_price
    
        return None
    
    @property
    def percentage_change(self):
        """Returns the percentage of change in price for the most recent log entry"""
        last_log = self.price_logs.first()
        if last_log:
            return ((last_log.new_price - last_log.old_price) / last_log.old_price) * 100
    
    @property
    def opening_price(self):
        """Returns the price at the start of the day"""
        today_logs = self.price_logs.filter(created_at__date=timezone.now().date()).order_by('created_at')
        if today_logs.exists():
            return today_logs.first().old_price
        
        return None
    
    @property
    def previous_close_price(self):
        """Returns the previous day's closing price"""
        yesterday = timezone.now().date() - timedelta(days=1)
        yesterday_logs = self.price_logs.filter(created_at__date=yesterday)
        
        if yesterday_logs.exists():
            return yesterday_logs.first().new_price
        return None

class PriceChangeLog(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT, related_name='price_logs')
    old_price = models.DecimalField(max_digits=15, decimal_places=2)
    new_price = models.DecimalField(max_digits=15, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at', '-updated_at']
        
        indexes = [
            models.Index(fields=['-created_at', '-new_price', 'old_price'])
        ]
    
    def __str__(self) :
        return f'Value of Stock changed from {self.old_price} {self.stock.currency} to {self.new_price} {self.stock.currency} for {self.stock.company_name} '