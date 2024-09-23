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