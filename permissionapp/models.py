from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from permissionapp.manager import CustomUserManager
import random
import string


class CustomUser( AbstractBaseUser, PermissionsMixin ):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("USER 1", "User 1"),
        ("USER 2", "User 2")
    )

    id = models.CharField( primary_key=True, max_length=8, unique=True )
    email = models.EmailField( max_length=50, unique=True )
    username = models.CharField( max_length=100, unique=True, default=True )
    password = models.CharField( max_length=100, null=True )
    first_name = models.CharField( max_length=50, null=True, blank=True )
    last_name = models.CharField( max_length=40, null=True, blank=True )
    created_at = models.DateTimeField( auto_now=True )
    updated_at = models.DateTimeField( auto_now=True )
    gender = models.CharField( max_length=8 )
    role = models.CharField( choices=ROLE_CHOICES, max_length=10, null=True )
    is_staff = models.BooleanField( default=False )
    is_superuser = models.BooleanField( default=False )
    is_active = models.BooleanField( default=True )
    phone_num = models.BigIntegerField( null=True, unique=True )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Products( models.Model ):
    product_name = models.CharField( max_length=30, null=True )
    product_price = models.IntegerField( null=True )
    product_description = models.CharField( max_length=100, null=True )
