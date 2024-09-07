from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from account.permissions import IsAdminOrGuardian
from blog.models import Post
from blog.views.post.serializer import PostSerializer


class PostCreateView(APIView):
    permission_classes = [IsAdminOrGuardian]

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Post created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'message': 'Post creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PostListView(ListAPIView):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {
            'message': 'List of published posts',
            'data': response.data
        }
        return response
    

class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'message': 'Post details retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class PostUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrGuardian]

    def get_queryset(self):
        if self.request.user.is_admin:
            return self.queryset
        return self.queryset.filter(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'message': 'Post updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'message': 'Post update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class PostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrGuardian]

    def get_queryset(self):
        if self.request.user.is_admin:
            return self.queryset
        return self.queryset.filter(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'message': 'Post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

