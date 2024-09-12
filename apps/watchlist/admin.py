from django.contrib import admin
from .models import Watchlist

# Register your models here.

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'stock', 'alert_price', 'created_at']
    list_filter = ['created_at', 'alert_price']
    search_fields = ['stock.tick','stock.company_name' ]
    
    date_hierarchy = 'created_at'
    ordering = ['created_at']