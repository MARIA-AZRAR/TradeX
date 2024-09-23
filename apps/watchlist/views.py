from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .permissions import isOwnerPermission
from .serializers import WatchlistSerializer
from .models import Watchlist

# Create your views here.

class WatchlistViewset(viewsets.ModelViewSet):
    
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated, isOwnerPermission]
    
    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = WatchlistSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
        
    def update(self, request, *args, **kwargs):
        instance = self.get_object() 

        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)