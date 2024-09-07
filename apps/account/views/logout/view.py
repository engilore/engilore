from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {"success": "Successfully logged out."},
                status=status.HTTP_200_OK
            )
        except AttributeError:
            return Response(
                {"error": "No active session found or already logged out."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred during logout.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
