# accounts/urls.py
from django.urls import path
from .viewsets import UserLoginApi

urlpatterns = [
    path('login/', UserLoginApi.as_view(), name='login'),
]