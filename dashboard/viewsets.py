# accounts/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from django.utils.crypto import get_random_string
from product.models import PasswordResetCode
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework import viewsets, status

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

from django.core.mail import send_mail
from django.utils.html import format_html


class ForgotPasswordApi(viewsets.ViewSet):
    def Generate(self, request):
        email = request.data.get("email")

        if not User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

        code = get_random_string(length=6, allowed_chars="0123456789")

        reset_code, created = PasswordResetCode.objects.update_or_create(
            email=email, defaults={"code": code}
        )
        # Send the email
        html_message = format_html(
            """
            <html>
            <body>
                <p>Your password reset code is:</p>
                <p style="color: red; font-size: 24px;"><strong>{code}</strong></p>
                <p>Do not share this code with anyone.</p>
            </body>
            </html>
            """, code=code
        )

        send_mail(
            subject="Password Reset Code",
            message=f"Your password reset code is: {code}. Do not share this code with anyone.",
            from_email="no-reply@example.com",
            recipient_list=[email],
            fail_silently=False,
            html_message=html_message,
        )


        return JsonResponse(
            {"message": "Reset code generated successfully"},
            status=status.HTTP_200_OK,
        )

    def verify(self, request):
        email = request.data.get("email")
        entered_code = request.data.get("code")

        try:
            reset_code = PasswordResetCode.objects.get(email=email, code=entered_code)
            reset_code.delete()

            return Response(
                {"message": "code validated successfully"}, status=status.HTTP_200_OK
            )
        except PasswordResetCode.DoesNotExist:
            return Response(
                {"error": "Invalid code or email"}, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Email does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

    
@api_view(["POST"])
# @permission_classes((IsAuthenticated,))
def resetpassword(request):
    email = request.data.get("email")
    new_password = request.data.get("new_password")
    confirm_password = request.data.get("confirm_password")

    # Basic validation
    if not email or not new_password or not confirm_password:
        return JsonResponse(
            {"error": "Email, new password, and confirm password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if new_password != confirm_password:
        return JsonResponse(
            {"error": "New password and confirm password do not match"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return JsonResponse(
            {"message": "Password changed successfully"}, status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return JsonResponse(
            {"error": "User not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Retrieve the token associated with the current user
            token = Token.objects.get(user=request.user)
            
            # Delete the token
            token.delete()
            
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        
        except Token.DoesNotExist:
            return Response({"detail": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)