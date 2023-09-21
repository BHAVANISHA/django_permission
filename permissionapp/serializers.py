from rest_framework import serializers
from .models import CustomUser, Products


class CustomUserSerializer( serializers.ModelSerializer ):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'gender', 'role', 'phone_num']


class Custom_login( serializers.Serializer ):
    email = serializers.CharField()
    password = serializers.CharField()


class Rice_serializer( serializers.ModelSerializer ):
    class Meta:
        model = Products
        fields = '__all__'


class IdSerializer( serializers.Serializer ):
    id = serializers.CharField()
