# accounts/urls.py
from django.urls import path
from .viewsets import CheckToken, ForgotPasswordApi, LogoutAPIView, UserLoginApi, resetpassword

urlpatterns = [
    path('login/', UserLoginApi.as_view(), name='login'),
    path("logout/", LogoutAPIView.as_view(), name="logout"),

    path("check-token/", CheckToken.as_view(), name="checks-expired-token"),
    
    path("forgot-password/generate/",ForgotPasswordApi.as_view({"post": "Generate"}), name="forgotpassword-generate"),
    path("forgot-password/verify/", ForgotPasswordApi.as_view({"post": "verify"}), name="forgotpassword-verify" ),
    path("reset-password/", resetpassword, name="resetpassword"),
]