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
        
class TransactionStatusUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transaction
        fields = ['status']
        
    def validate_status(self, value):
        if value not in [Transaction.StatusTypes.COMPLETED or Transaction.StatusTypes.FAILED]:
            raise serializers.ValidationError("Status can only be set to complete or failed")
        return value
        