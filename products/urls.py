from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('product',ProductsViewSet.as_view(
        {
        'get': 'list',
        'post': 'create'
        
    })),
    path('product/<str:pk>',ProductsViewSet.as_view(
        {
        'get': 'retrieve',
        'put':'update',
        'destroy':'delete'
    })),
    
    path('category',
         CategoriesViewSet.as_view(
        {
        'get': 'list',
        'post': 'create'
    })),
    path('category/<str:pk>', CategoriesViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('review',
         ReviewViewSet.as_view(
        {
        'get': 'list',
        'post': 'create'
    })),
    path('review/<str:pk>', ReviewViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    
]
