from django.db import models
from common import constants

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
    tick = models.CharField(max_length=50, null=False ,unique=True) 
    description = models.TextField()
    volume = models.BigIntegerField()
    current_price = models.DecimalField(max_digits=15, decimal_places=2)
    outstanding_shares = models.BigIntegerField()
    list_date = models.DateField()
    stock_type = models.CharField(max_length=20, choices=StockTypes.choices)
    currency = models.CharField(max_length=20, choices=constants.CURRENCY_CHOICES)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
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
    
    