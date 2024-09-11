from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from account.models import User
from account.views.serializer import UserSerializer
from account.permissions import IsAdmin


class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            'message': 'List of all users',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response({
            'message': 'User details retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def put(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'User update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        
        if user.is_admin:
            return Response({
                'message': 'You cannot delete an admin user.'
            }, status=status.HTTP_403_FORBIDDEN)

        user.delete()
        return Response({
            'message': 'User deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class UserRoleAssignView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        role = request.data.get('role')

        if role == 'admin':
            return Response({
                'message': 'You are not allowed to assign the admin role.'
            }, status=status.HTTP_403_FORBIDDEN)

        if role == 'guardian':
            user.is_guardian = True
        elif role == 'auxiliary':
            user.is_auxiliary = True
        else:
            return Response({
                'message': 'Invalid role provided'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.save()
        return Response({
            'message': f'Role "{role}" assigned successfully to user {user.username}'
        }, status=status.HTTP_200_OK)



class UserRoleRevokeView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk, format=None):
        user = get_object_or_404(User, pk=pk)
        role = request.data.get('role')

        if role == 'admin' and user == request.user:
            return Response({
                'message': 'You cannot revoke the admin role from yourself.'
            }, status=status.HTTP_403_FORBIDDEN)

        if role == 'admin':
            user.is_admin = False
        elif role == 'guardian':
            user.is_guardian = False
        elif role == 'auxiliary':
            user.is_auxiliary = False
        else:
            return Response({
                'message': 'Invalid role provided'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.save()
        return Response({
            'message': f'Role "{role}" revoked successfully from user {user.username}'
        }, status=status.HTTP_200_OK)
