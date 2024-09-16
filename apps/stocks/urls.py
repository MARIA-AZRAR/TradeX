from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import StockViewSet, PriceHistoryView


router = DefaultRouter()

router.register(r'stocks', viewset=StockViewSet, basename='stocks')

urlpatterns = [
    path('stocks/history/', view=PriceHistoryView.as_view(), name='price-history'),
    path('', include(router.urls))
]