from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()