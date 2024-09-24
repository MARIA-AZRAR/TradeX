from django.urls import path
from .views import LogoutView, UserRegistrationView, LoginView, AccountListView

urlpatterns = [
    path('auth/registration', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/logout', LogoutView.as_view(), name='logout'),
    path('user/account', AccountListView.as_view(), name='account')
]