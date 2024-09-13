from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    market_cap = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    price_change = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    percentage_change = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)
    opening_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    previous_close_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Stock
        fields = [
            'company_name', 'tick', 'description', 'current_price', 'volume', 'outstanding_shares', 
            'currency', 'stock_type', 'market_cap', 'price_change', 'percentage_change', 'opening_price', 
            'previous_close_price', 'list_date', 'is_active'
        ]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if self.context.get('request').method == 'GET':
            representation['currency'] = instance.get_currency_display() 
            representation['stock_type'] = instance.get_stock_type_display()
        
        return representation
    
    
    