from rest_framework import serializers

from category.views.category.serializer import CategorySerializer
from category.views.topic.serializer import TopicSerializer
from blog.models import Post


class FeaturedPostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    topics = TopicSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'slug',
            'title',
            'summary',
            'content',
            'featured_image',
            'category',
            'topics',
            'status',
            'type',
            'meta_title',
            'meta_description',
            'is_featured',
            'published_at',
            'created_at',
            'updated_at',
        ]