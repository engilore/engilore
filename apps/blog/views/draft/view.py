from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsAdminOrGuardian
from blog.models import Post
from blog.views.serializer import PostSerializer


class PostDraftListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrGuardian]

    def get(self, request, format=None):
        posts = Post.objects.filter(status='draft', author=request.user)
        serializer = PostSerializer(posts, many=True)
        return Response({
            'message': 'List of draft posts',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PostDraftDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrGuardian]

    def get_object(self, id, request):
        try:
            return Post.objects.get(id=id, status='draft', author=request.user)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        post = self.get_object(id, request)
        serializer = PostSerializer(post)
        return Response({
            'message': 'Draft post details retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PostDraftUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrGuardian]

    def get_object(self, id, request):
        try:
            return Post.objects.get(id=id, status='draft', author=request.user)
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        post = self.get_object(id, request)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Draft post updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Draft post update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PostDraftDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrGuardian]

    def get_object(self, id, request):
        try:
            return Post.objects.get(id=id, status='draft', author=request.user)
        except Post.DoesNotExist:
            raise Http404

    def delete(self, request, id, format=None):
        post = self.get_object(id, request)
        post.delete()
        return Response({
            'message': 'Draft post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
