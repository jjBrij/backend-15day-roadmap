from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView as apiView
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from django.contrib.auth.models import User
from.serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny




class RegisterView(generics.CreateAPIView):
    quaryset = User.objects.all()
    serializer_class = RegisterSerializer
 #

class loginView(generics.GenericAPIView):
     serializer_class = LoginSerializer


     def post(self, request, *args, **kwargs):
          username = request.data.get('username')
          password = request.data.get('password')
          User = authenticate(username=username, password=password)
          if User is not None:
               refresh = RefreshToken.for_user(User)
               userserializer = UserSerializer(User)
               return Response({
                    'user': userserializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
          else:
                
                return Response({'error': 'Invalid Credentials'}, status=400)
          
class DashboardView(apiView):
    permission_classes = [IsAuthenticated]

    def get(self, request):        
         User = request.user
         userserializer = UserSerializer(User)
         return Response({'message': 'Welcome to the dashboard!', 'user': userserializer.data})
         
    