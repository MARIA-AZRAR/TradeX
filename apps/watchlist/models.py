from django.db import models
from apps.stocks.models import Stock
from django.conf import settings
# Create your models here.

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