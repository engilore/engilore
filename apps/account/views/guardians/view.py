from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from account.models import User
from account.views.guardians.serializer import GuardianSerializer


class GuardianListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        guardians = User.objects.filter(is_guardian=True)
        serializer = GuardianSerializer(guardians, many=True)
        return Response({
            'message': 'List of guardians retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
