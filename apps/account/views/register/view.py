from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.authtoken.models import Token

from apps.account.views.serializer import UserSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data

            return Response(
                {
                    "success": "User registered successfully",
                    "token": token.key,
                    "user": user_data,
                },
                status=status.HTTP_201_CREATED
            )

        return Response({
            "error": "Invalid data",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)