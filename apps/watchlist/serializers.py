from rest_framework import serializers

from apps.stocks.models import Stock
from apps.stocks.serializers import StockSerializer
from .models import Watchlist


class WatchlistSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    stock = serializers.PrimaryKeyRelatedField(queryset=Stock.active_objects.all())

    class Meta:
        model = Watchlist
        fields = ['user', 'alert_price', 'stock']
        
    def validate(self, data):
        # Check if the user already has this stock in their watchlist
        if self.context.get('request').method == 'POST':
            user = self.context['request'].user
            stock = data['stock']

            if Watchlist.objects.filter(user=user, stock=stock).exists():
                raise serializers.ValidationError("This stock is already in your watchlist.")
            
        return data