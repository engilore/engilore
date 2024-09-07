from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        if not user:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        password = request.data.get('password')
        if not password:
            return Response(
                {"error": "Password is required to delete the account."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(password):
            return Response(
                {"error": "Password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user.delete()
            return Response(
                {"success": "User deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": "Failed to delete user due to an unexpected error.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
