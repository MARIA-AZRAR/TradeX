from django.urls import path
from .views import UserRegistrationView

urlpatterns = [
    path('auth/registration', UserRegistrationView.as_view(), name='user-registration')
]