from rest_framework import serializers
from category.models import Category, Topic


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


class TopicSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_details = serializers.SerializerMethodField()
    created_by = serializers.ReadOnlyField(source='created_by.first_name')

    class Meta:
        model = Topic
        fields = [
            'id', 'name', 'description', 'slug', 
            'category', 'category_details',
            'meta_title', 'meta_description',
            'created_by', 'created_at', 'updated_at'
        ]

    def get_category_details(self, obj):
        if obj.category:
            return CategorySerializer(obj.category).data
        return None