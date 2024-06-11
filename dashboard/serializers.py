from django.http import HttpRequest
from django.urls import NoReverseMatch, reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]
        extra_kwargs = {
            "email": {"write_only": True, "required": True},
            "username": {"write_only": True, "required": True},
            "password": {"write_only": True, "required": True},
            "date_joined": {"write_only": True, "required": False},
        }