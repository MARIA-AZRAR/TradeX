from django.urls import path
from .views import AdminPortfolioView, UserPortfolioView, TransactionView, TransactionStatusView, TransactionListView

urlpatterns = [
    path('portfolios/', view=UserPortfolioView.as_view(), name='portfolio'),
    path('api/admin/portfolios/', view=AdminPortfolioView.as_view(), name='admin-portfolio'),
    path('transaction/', view= TransactionListView.as_view(), name='transaction'),
    path('transaction/<int:pk>/', view= TransactionListView.as_view(), name='transaction-detail'),
    path('make-transaction/', view=TransactionView.as_view(), name='make-transaction'),
    path('transaction/<int:pk>/update-status/', TransactionStatusView.as_view(), name='transaction-update-status'), 
]