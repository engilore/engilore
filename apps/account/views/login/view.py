from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token

from account.models import User
from account.views.serializer import UserSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username_or_email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=username_or_email, password=password)
        
        if not user:
            try:
                user = User.objects.get(email=username_or_email)
                user = authenticate(username=user.username, password=password)
                if not user:
                    return Response(
                        {"error": "Invalid credentials. Please check your password."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid credentials. User not found."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if user and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data

            return Response(
                {
                    "token": token.key,
                    "user": user_data,
                },
                status=status.HTTP_200_OK
            )
        elif user and not user.is_active:
            return Response(
                {"error": "Account is disabled."},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_400_BAD_REQUEST
        )