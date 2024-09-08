from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny

from account.permissions import IsAdminOrGuardian
from blog.models import Post
from blog.views.post.serializer import PostSerializer


class PostCreateView(APIView):
    permission_classes = [IsAdminOrGuardian]

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({
                'message': 'Post created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'message': 'Post creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PostListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        posts = Post.objects.filter(status='published')
        serializer = PostSerializer(posts, many=True)
        return Response({
            'message': 'List of published posts',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PostDetailView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, id):
        try:
            return Post.objects.get(id=id, status='published')
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        post = self.get_object(id)
        serializer = PostSerializer(post)
        return Response({
            'message': 'Post details retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PostUpdateView(APIView):
    permission_classes = [IsAdminOrGuardian]

    def get_object(self, id, request):
        try:
            post = Post.objects.get(id=id)
            if request.user.is_admin or post.author == request.user:
                return post
            else:
                raise PermissionDenied("You do not have permission to edit this post.")
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, id, format=None):
        post = self.get_object(id, request)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Post updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Post update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    

class PostDeleteView(APIView):
    permission_classes = [IsAdminOrGuardian]

    def get_object(self, id, request):
        try:
            post = Post.objects.get(id=id)
            if request.user.is_admin or post.author == request.user:
                return post
            else:
                raise PermissionDenied("You do not have permission to delete this post.")
        except Post.DoesNotExist:
            raise Http404

    def delete(self, request, id, format=None):
        post = self.get_object(id, request)
        post.delete()
        return Response({
            'message': 'Post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
