from django.contrib import admin
from .models import Profile, Account

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'phone_number', 'created_at', 'is_active']
    list_filter = ['created_at', 'is_active']
    search_fields = ['user.username']
    
    date_hierarchy = 'created_at'
    ordering = ['created_at', 'is_active']

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'currency']
   