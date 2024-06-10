from rest_framework import viewsets
from django.http import HttpResponse
def home(self):
    return HttpResponse('hello i am nishant timsina')