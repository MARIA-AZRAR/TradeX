from django.contrib import admin
from .models import Portfolio, Transaction
# Register your models here.

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock', 'quantity', 'purchase_price' ,'created_at']
    list_filter = ['created_at', 'purchase_price', 'stock']
    search_fields = ['stock.tick','stock.company_name' ]
    
    date_hierarchy = 'created_at'
    ordering = ['created_at']
    
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock', 'price_at_transaction', 'quantity', 'transaction_type', 'status', 'created_at']
    list_filter = ['status', 'transaction_type', 'created_at', 'price_at_transaction', 'stock']
    search_fields = ['transaction_type', 'status' ]
    
    date_hierarchy = 'created_at'
    ordering = ['created_at']