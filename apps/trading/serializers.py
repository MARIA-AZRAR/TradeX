from rest_framework import serializers

from apps.stocks.serializers import StockSerializer
from .models import Portfolio, Transaction

class PortfolioSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    stock = StockSerializer()
    class Meta:
        model = Portfolio
        fields = ['user', 'quantity', 'purchase_price', 'current_value', 'profit_loss', 'stock']

    
class TransactionSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(choices=Transaction.TransactionTypes.choices, required=True)
    stock_symbol = serializers.CharField(max_length=50, required=True)
    quantity = serializers.IntegerField(required=True)
    
    class Meta:
        fields = ['quantity' ,'transaction_type', 'stock_symbol']