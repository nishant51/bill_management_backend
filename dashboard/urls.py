# accounts/urls.py
from django.urls import path
from .viewsets import CheckToken, UserLoginApi

urlpatterns = [
    path('login/', UserLoginApi.as_view(), name='login'),
    path("check-token/", CheckToken.as_view(), name="checks-expired-token"),

]