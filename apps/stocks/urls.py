from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockViewSet


router = DefaultRouter()

router.register(r'stocks', viewset=StockViewSet, basename='stocks')



urlpatterns = [
    path('', include(router.urls)),
]