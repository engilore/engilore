from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.views.serializer import UserSerializer


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data.copy()

        sensitive_fields = ['password', 'email']
        updating_sensitive = any(field in data for field in sensitive_fields)

        if updating_sensitive:
            current_password = request.data.get('current_password')

            if not current_password:
                return Response(
                    {"error": "You must provide your current password to update sensitive information."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not user.check_password(current_password):
                return Response(
                    {"error": "Current password is incorrect."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            new_password = request.data.get('new_password')
            if new_password:
                user.set_password(new_password)
                user.save()

        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "Profile updated successfully."},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "Invalid data", "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )