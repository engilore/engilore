from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


from account.permissions import IsAdmin, IsAdminOrGuardian
from category.models import Topic
from category.views.topic.serializer import TopicSerializer



class TopicListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class TopicCreateView(APIView):
    permission_classes = [IsAdminOrGuardian]

    def post(self, request, format=None):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Topic created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Topic creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TopicDetailView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        topic = self.get_object(pk)
        serializer = TopicSerializer(topic)
        return Response(serializer.data)


class TopicUpdateView(APIView):
    permission_classes = [IsAdminOrGuardian]

    def get_object(self, pk):
        try:
            return Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        topic = self.get_object(pk)
        serializer = TopicSerializer(topic, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Topic updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Topic update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class TopicDeleteView(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        topic = self.get_object(pk)
        topic.delete()
        return Response({
            'message': 'Topic deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
