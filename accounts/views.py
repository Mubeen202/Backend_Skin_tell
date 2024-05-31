from typing import Any, Optional
import datetime
from django.db.models import Q, Count
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import parsers, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from json import JSONEncoder
from uuid import UUID
import __future__ 
from .models import *
from .renderers import UserJSONRenderer
from .serializers import *
from django.contrib.auth.hashers import make_password
from typing import Tuple, Dict
class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request: Request) -> Response:
        """Return user response after a successful registration."""
        user_request = request.data.get('user', {})  # Include the entire request.data
        is_superuser = user_request.pop('is_superuser', False)
        if request.user.is_authenticated:
            return Response({'message': 'User is already logged in', 'error': True, 'code': 400})
        if is_superuser:
            user_request['user_created_by'] = None
            user_request['is_superuser'] = True
        else:
            user_request['is_simpleuser'] = True
        
        serializer = self.serializer_class(data=user_request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class RegistrationUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserRegistrationSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        """Handle user registration."""
        user_request = request.data.get('user', {})
        
        # Check if the current user is a superuser
        if request.user.is_superuser:
            # Retrieve the user instance of the user who is creating the new user
            user_created_by = str(request.user.id)
            user_request['user_created_by'] = user_created_by
            user_request['is_simpleuser'] = True
            
            # Create a serializer instance with the provided data
            serializer = self.serializer_class(data=user_request)
            
            # Validate the serializer
            if serializer.is_valid():
                # If validation succeeds, save the user
                user = serializer.save()
                print('serializer', serializer.data)
                return Response({'message': 'User created successfully.', 'error': False, 'user': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                # If validation fails, return detailed error messages
                return Response({'message': 'Failed to create user.', 'error': True, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Return an error response if the user is not a superuser
            return Response({'message': 'You are not authorized to create a new user.', 'error': True}, status=status.HTTP_403_FORBIDDEN)

    

class UpdateUserByIdAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserRegistrationSerializer
    lookup_url_kwarg = 'id'
    parser_classes = [
        parsers.JSONParser,
        parsers.FormParser,
        parsers.MultiPartParser,
    ]

       
        
    def patch(self, request: Request , pk=None) -> Response:
        """Return user response after a successful registration."""
        clients = User.objects.get(id=pk)
        serializer_data = request.data.get('user', {})
        # serializer = UserRegistrationSerializer(clients, data=serializer_data, partial=True)
        # if serializer.is_valid():
        #     user = serializer.save()
        #     return Response(UserRegistrationSerializer(user).data)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(clients,data=serializer_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """Return user after login."""
        user = request.data.get('user', {})

       
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    lookup_url_kwarg = 'id'
    parser_classes = [
        parsers.JSONParser,
        parsers.FormParser,
        parsers.MultiPartParser,
    ]

    def get(self, request: Request, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Response:
        """Get request."""
        serializer = self.serializer_class(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, *args: Tuple[Any], **kwargs: Dict[str, Any]) -> Response:
        """Patch method."""
        serializer_data = request.data.get('user', {})
        serializer = UserSerializer(request.user, data=serializer_data, partial=True)
        
        

        if serializer.is_valid():
            # old_default = JSONEncoder.default
            # def new_default(self, users):
            #     if isinstance(users, UUID):
            #         return str(users)
            #     return old_default(self, users)
            # JSONEncoder.default = new_default
            user = serializer.save()
            print('jjlkjlkjlk', user)
            

            return Response(UserSerializer(user).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



   

class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Validate token and save."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message':'Logged Out Successfully'}, status=status.HTTP_204_NO_CONTENT)

class FetchUsers(viewsets.ViewSet):
    permission_classes =  (IsAuthenticated ,)
    def list(self, request):
        username_contain = request.GET.get('username')
        query = Q()
        if username_contain:
            query &= Q(username__icontains=username_contain)
        if request.user.is_staff:
            client = User.objects.all().filter(query,is_active=True, is_staff = False ).distinct()[:300000]
        else:
            client = User.objects.all().filter(query,is_active=True, user_created_by=request.user.id).distinct()[:300000]
        serializer = GettingUserRegistrationSerializer(client, many=True)
        if serializer:
            return Response({'message':'Users Fetch Successfully','error':False,'code':200,'result':{'totalItems':len(serializer.data),'items':serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'Some thing went Wrong in Fetching Users','error':True,'code':400,'result':{'items':serializer.errors}},status=status.HTTP_400_BAD_REQUEST)
    

 
    def retrieve(self, request, pk=None):
        clients = User.objects.get(id=pk)
        serializer = GettingUserRegistrationSerializer(clients)
        if serializer:
            return Response({'message':'User  Fetch Successfully','error':False,'code':200,'result':{'totalFields':len(serializer.data),'items':serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'Some thing went Wrong in Fetching User ','error':True,'code':400,'result':{'items':serializer.errors}},status=status.HTTP_400_BAD_REQUEST)
   



