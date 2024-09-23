from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import WatchlistViewset


router = DefaultRouter()

router.register(r'watchlist', viewset=WatchlistViewset, basename='watchlist')

urlpatterns = [
    path('', include(router.urls))
]