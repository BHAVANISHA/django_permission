from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework import status
from .models import *
from permissionapp import models, serializers
from django.contrib.auth.models import Group, Permission
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView


class Registration( CreateAPIView ):
    serializer_class = serializers.CustomUserSerializer

    def generate_random_user_id(self):
        letters = "CID"
        numbers = ''.join( random.choice( string.digits ) for _ in range( 5 ) )
        return letters + numbers
    print('hello')

    def post(self, request, *args, **kwargs):
        try:
            serializer_class = serializers.CustomUserSerializer( data=request.data )
            hashpass = make_password( request.data['password'] )
            if serializer_class.is_valid():
                serializer_class.validated_data['id']  = self.generate_random_user_id()
                serializer_class.save( password=hashpass )
                role = request.data.get( 'role', None )
                user = CustomUser.objects.get( email=request.data['email'] )
                if role not in ('ADMIN', 'USER 1', 'USER 2'):
                    return Response(
                        {'message': 'Invalid role provided'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    if role == 'ADMIN':
                        admin_group, created = Group.objects.get_or_create( name='ADMIN' )
                        permissions = ['add_products', 'view_products', 'change_products', 'delete_products']
                        for codename in permissions:
                            perm = Permission.objects.get( codename=codename )
                            admin_group.permissions.add( perm )
                        admin_group.save()
                        user.groups.add( admin_group )

                    elif role == 'USER 1':
                        user1_group, created = Group.objects.get_or_create( name='USER 1' )
                        permissions = ['add_products', 'view_products']
                        for codename in permissions:
                            perm = Permission.objects.get( codename=codename )
                            user1_group.permissions.add( perm )
                        user1_group.save()
                        user.groups.add( user1_group )

                    elif role == 'USER 2':
                        user2_group, created = Group.objects.get_or_create( name='USER 2' )
                        permissions = ['add_products', 'view_products', 'change_products']
                        for codename in permissions:
                            perm = Permission.objects.get( codename=codename )
                            user2_group.permissions.add( perm )
                        user2_group.save()
                        user.groups.add( user2_group )

                    data = {
                        'Response Code': status.HTTP_201_CREATED,
                        'Status': 'TRUE',
                        'Message': 'User Details Created Successfully',
                        "Error": 'None',
                        "StatusFlag": True,
                        'Data': serializer_class.data,
                    }
                    return Response( data )
            else:
                dataa = {
                    'response_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Phone number,username already exists',
                    'statusFlag': False,
                    'status': 'FAILURE',
                    'errorDetails': 'Change username or password',
                    'data': ""
                }
                return Response( dataa )
        except Exception as e:
            data = {
                'Response Code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'Status': 'FALSE',
                'Message': 'Creating Process is failed',
                "Error": str( e ),
                "StatusFlag": False,
                'Data': [],
            }
            return Response( data )


class Login( CreateAPIView ):
    serializer_class = serializers.Custom_login

    def post(self, request, *args, **kwargs):
        try:
            auth = authenticate( email=request.data['email'], password=request.data['password'] )
            # user = CustomUser.objects.get( email=request.data['email'])
            if auth:
                token, create = Token.objects.get_or_create( user=auth )

                data = {
                    'response_code': status.HTTP_202_ACCEPTED,
                    'message': 'Login successful',
                    'status': 'SUCCESS',
                    'error details': 'NONE',
                    'data': []
                }
                return Response( data )
        except Exception as e:
            dataa = {
                'response_code': status.HTTP_404_NOT_FOUND,
                'message': 'Login unsuccessful',
                'status': 'FAILURE',
                'error details': str( e ),
                'data': ""
            }
            return Response( dataa )


class RiceCreateView( CreateAPIView ):
    serializer_class = serializers.Rice_serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [DjangoModelPermissions]
    queryset = models.Products.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            serializer = serializers.Rice_serializer( data=request.data )
            if serializer.is_valid():
                serializer.save()
                data = {
                    'response_code': status.HTTP_202_ACCEPTED,
                    'message': "Product added successfully",
                    'status': 'SUCCESS',
                    'errorDetails': "NONE",
                    'data': serializer.data
                }
                return Response( data )
            else:
                data = {
                    'response_code': status.HTTP_400_BAD_REQUEST,
                    'message': "Invalid data provided",
                    'status': 'FAILURE',
                    'errorDetails': serializer.errors,
                    'data': None
                }
                return Response( data, status=status.HTTP_400_BAD_REQUEST )
        except Exception as e:
            dataa = {
                'response_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': "Internal server error",
                'status': 'FAILURE',
                'errorDetails': str( e ),
                'data': None
            }
            return Response( dataa, status=status.HTTP_500_INTERNAL_SERVER_ERROR )


class View_all_item( ListAPIView ):
    serializer_class = serializers.Rice_serializer
    queryset = models.Products.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        return self.list( request, *args, **kwargs )


class View_particular_item( RetrieveAPIView ):
    serializer_class = serializers.Rice_serializer
    queryset = models.Products.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        return self.retrieve( request, *args, **kwargs )


class Delete_product( GenericAPIView ):
    serializer_class = serializers.Rice_serializer
    queryset = models.Products.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, id, *args, **kwargs):
        query = models.Products.objects.get( id=id )
        query.delete()
        return Response( 'deleted' )


class Update_product( UpdateAPIView ):
    serializer_class = serializers.Rice_serializer
    queryset = models.Products.objects.all()
    permission_classes = [DjangoModelPermissions]
    authentication_classes = [TokenAuthentication]

    def put(self, request, *args, **kwargs):
        return self.update( request, *args, **kwargs )


