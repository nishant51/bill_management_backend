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
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone

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
        
class CheckToken(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.auth
        user = request.user
        if token and token.created:
            if token.created < (timezone.now() - timezone.timedelta(days=1)):
                return Response({"message": "Token has expired"}, status=401)
        return Response(
            {"message": "Token is valid"}, status=200
        )