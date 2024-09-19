from django.urls import path
from .views import AdminPortfolioView, UserPortfolioView, TransactionView, TransactionStatusView

urlpatterns = [
    path('portfolios/', view=UserPortfolioView.as_view(), name='portfolio'),
    path('api/admin/portfolios/', view=AdminPortfolioView.as_view(), name='admin-portfolio'),
    path('transaction/', view=TransactionView.as_view(), name='transaction'),
    path('transaction/<int:pk>/update-status/', TransactionStatusView.as_view(), name='transaction-update-status'), 
]