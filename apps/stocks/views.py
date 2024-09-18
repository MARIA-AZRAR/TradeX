from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import PriceChangeSerializer, StockSerializer
from .models import PriceChangeLog, Stock

# Create your views here.

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.active_objects.all()
    serializer_class = StockSerializer


    def destroy(self, request, *args, **kwargs):
         """Set the is_active to false in order to soft delete"""
         instance = self.get_object()
         instance.is_active = False
         instance.save()
         
         return Response(status=status.HTTP_204_NO_CONTENT)
     
    def get_permissions(self):
        """ Return permission based on action"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdminUser] 
        
        else:
               self.permission_classes = [IsAuthenticated]          
        return super().get_permissions()


class PriceHistoryView(generics.ListAPIView):
    serializer_class = PriceChangeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        tick = self.request.query_params.get('symbol')
        
        if not tick:
            return Response({'error': 'symbol is required'}, status=400)
        
        stock = get_object_or_404(Stock, tick=tick, is_active= True)
        
        return PriceChangeLog.objects.filter(stock=stock)
     
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)