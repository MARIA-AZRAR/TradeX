from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime
from .models import Profile

        
class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, max_length=30)
    date_of_birth = serializers.DateField(required=False)
    address = serializers.CharField(required=True, max_length=250, write_only=True)
    
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True, label = 'Confirm Password')
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'address', 'password', 'password2']
        
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
             raise serializers.ValidationError('Account Already exists with this email')
        return value
    
    def validate_date(self, value):
        if value:
            if value > datetime.today().date():
                raise serializers.ValidationError('Please enter another date')
        return value
    
    def validate_phone_number(self, value):
        if value:
            if not value.isdigit():
                raise serializers.ValidationError('Please enter digits only')
        return value
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number', None)
        date_of_birth = validated_data.pop('date_of_birth', None)
        address = validated_data.pop('address', None)
        password = validated_data.pop('password', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        
        user = User (
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = first_name,
            last_name = last_name
        )
        
        user.set_password(password)
        user.save()
        
        Profile.objects.create(
            user=user,
            date_of_birth=date_of_birth,
            address=address,
            phone_number=phone_number
        )
        
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        print(self.context)
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("user is inactive")
            else: 
                raise serializers.ValidationError("no user with such username and password")
        else: 
            raise serializers.ValidationError("Username or Password is empty")
        
        attrs['user'] = user
        return attrs
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']