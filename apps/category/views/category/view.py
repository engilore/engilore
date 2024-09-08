from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from account.permissions import IsAdmin, IsAdminOrGuardian
from category.models import Category
from category.views.category.serializer import CategorySerializer



class CategoryListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryCreateView(APIView):
    permission_classes = [IsAdminOrGuardian]

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Category created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Category creation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


class CategoryUpdateView(APIView):
    permission_classes = [IsAdminOrGuardian]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Category updated successfully',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Category update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CategoryDeleteView(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response({
            'message': 'Category deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)
