from rest_framework import serializers
from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.first_name')
    topics = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'slug', 
            'meta_title', 'meta_description', 
            'topics', 'created_by', 'created_at', 'updated_at'
        ]


