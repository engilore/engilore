from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from account.permissions import IsAdmin
from blog.models import Post
from blog.views.featured.serializer import FeaturedPostSerializer



class FeaturedPostView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            featured_post = Post.objects.filter(is_featured=True).first()
            if not featured_post:
                return Response(
                    {'message': 'No featured post found.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = FeaturedPostSerializer(featured_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ToggleFeaturePostView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            if not post.is_featured:
                Post.objects.filter(is_featured=True).update(is_featured=False)
                post.is_featured = True
            else:
                post.is_featured = False

            post.save()

            return Response({
                'message': 'Post updated successfully',
                'is_featured': post.is_featured
            }, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {'error': f'An error occurred: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
