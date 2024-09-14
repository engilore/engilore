from rest_framework import serializers

from category.models import Category, Topic

from blog.models import Post
from blog.views.serializer import AuthorSerializer

class PostDraftSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Category.objects.all(),
        required=False
    )
    topics = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Topic.objects.all(),
        required=False
    )

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'volume',
            'summary',
            'content',
            'category',
            'topics',
            'status',
            'type',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
