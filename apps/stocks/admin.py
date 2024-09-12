from django.contrib import admin
from .models import Stock, PriceChangeLog
# Register your models here.

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'tick', 'current_price', 'volume', 'outstanding_shares', 'currency', 'is_active']
    list_filter = ['is_active', 'created_at', 'tick', 'current_price', 'currency']
    search_fields = ['company_name', 'tick']
    
    date_hierarchy = 'created_at'
    ordering = ['created_at', 'current_price']
    
    

@admin.register(PriceChangeLog)
class PriceLogAdmin(admin.ModelAdmin):
    list_display = ['stock', 'old_price', 'new_price', 'created_at']
    list_filter = ['created_at', 'old_price', 'new_price']
    search_fields = ['stock']
    
    date_hierarchy = 'created_at'
    ordering = ['created_at', 'new_price']