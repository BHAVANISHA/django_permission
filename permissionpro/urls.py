"""
URL configuration for permissionpro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from permissionapp import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact( email="contact@snippets.local" ),
        license=openapi.License( name="BSD License" ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path( 'register/', views.Registration.as_view() ),
    path('login/',views.Login.as_view()),
    path('listpro/',views.View_all_item.as_view()),
    path('deletepro/<int:id>',views.Delete_product.as_view()),
    path('updatepro/<int:pk>',views.Update_product.as_view()),
    path('createpro/',views.RiceCreateView.as_view()),
    path('retreivepro/<int:pk>',views.View_particular_item.as_view()),
    path( 'swagger/', schema_view.with_ui( 'swagger', cache_timeout=0 ), name='schema-swagger-ui' ),


]
