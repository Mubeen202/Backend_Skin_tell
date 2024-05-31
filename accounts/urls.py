from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name='register_user'),
    path('userRegister', RegistrationUserAPIView.as_view(), name='register_user'),
    path('updateUser/<str:pk>', UpdateUserByIdAPIView.as_view(), name='register_user'),
    path('login', LoginAPIView.as_view(), name='login_user'),
    path('logout', LogoutAPIView.as_view(), name="logout_user"),
    path('information', UserRetrieveUpdateAPIView.as_view(), name='user'),  # kwargs={'id': None},
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('users',FetchUsers.as_view(
        {
        'get': 'list',
        
    })),
    path('user/<str:pk>',FetchUsers.as_view(
        {
        'get': 'retrieve',
    })),
    
]
