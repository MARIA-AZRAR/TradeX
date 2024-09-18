from django.urls import path
from .views import UserRegistrationView, LoginView

urlpatterns = [
    path('auth/registration', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/login', LoginView.as_view(), name='login')
]