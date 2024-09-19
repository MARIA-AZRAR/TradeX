from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.stocks.models import Stock
from apps.trading.services import handle_transaction, handle_transaction_status
from apps.users.models import Account
from .serializers import PortfolioSerializer, TransactionSerializer, TransactionStatusUpdateSerializer
from .models import Portfolio, Transaction
# Create your views here.

class UserPortfolioView(generics.ListAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

class AdminPortfolioView(generics.ListAPIView):
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Portfolio.objects.all()

class TransactionView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            stock = get_object_or_404(Stock, tick=serializer.validated_data['stock_symbol'])
            account = get_object_or_404(Account, user=user)
            quantity = serializer.validated_data['quantity']
            transaction_type = serializer.validated_data['transaction_type']
            try:
                handle_transaction(user, stock, account, quantity, transaction_type)
                
                return Response({"success": "Transaction Completed"}, status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    
class TransactionStatusView(generics.UpdateAPIView):
    serializer_class = TransactionStatusUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Transaction.objects.all()
    
    def update(self, request, *args, **kwargs):
        transaction = self.get_object()
        
        if transaction.status != Transaction.StatusTypes.PENDING:
            return Response({"error": "Only pending transactions can be updated."}, status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            transaction_status = serializer.validated_data['status']
            account = get_object_or_404(Account, user=transaction.user)
            try:
                response = handle_transaction_status(transaction, transaction_status, account)
                if 'error' in response:
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
                return Response(response, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status.HTTP_400_BAD_REQUEST)
           
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)