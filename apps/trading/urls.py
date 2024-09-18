from django.urls import path
from .views import AdminPortfolioView, UserPortfolioView, TransactionView

urlpatterns = [
    path('portfolios/', view=UserPortfolioView.as_view(), name='portfolio'),
    path('api/admin/portfolios/', view=AdminPortfolioView.as_view(), name='admin-portfolio'),
    path('transaction/', view=TransactionView.as_view(), name='transaction') 
]