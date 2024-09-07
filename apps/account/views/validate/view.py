from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.account.views.serializer import UserSerializer


class ValidateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_data = UserSerializer(request.user).data
        return Response({
            'message': 'Token is valid',
            'user': user_data
        }, status=status.HTTP_200_OK)
