from rest_framework import serializers
from category.models import Topic, Category


class TopicSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.first_name')
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Topic
        fields = [
            'id', 'name', 'description', 'slug', 
            'category', 'meta_title', 'meta_description',
            'created_by', 'created_at', 'updated_at'
        ]
