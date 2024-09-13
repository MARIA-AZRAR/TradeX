from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockViewSet, PriceHistoryView


router = DefaultRouter()

router.register(r'stocks', viewset=StockViewSet, basename='stocks')



urlpatterns = [
    path('', include(router.urls)),
    path('stock/history/', view=PriceHistoryView.as_view(), name='price-history')
]