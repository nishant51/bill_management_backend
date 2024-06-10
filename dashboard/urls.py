from django.urls import path,include
from .viewsets import *
urlpatterns = [
    path('home/',home)
]