# accounts/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.db.models import Q

class UserLoginApi(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        if user and user.check_password(password):
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            response_data = {
                "status": 200,
                "message": "Login successful",
                "token": token.key,
                "username":username,
                "user": UserSerializer(user).data,
            }
            return Response(response_data)
        else:
            return Response({"error": "Invalid credentials"}, status=401)