from rest_framework import serializers

from category.models import Category, Topic

from blog.models import Post
from blog.views.serializer import AuthorSerializer



class PostSerializer(serializers.ModelSerializer):
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
            'slug',
            'title',
            'volume',
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
        read_only_fields = ['author', 'slug', 'created_at', 'updated_at', 'status',]

    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        topics = validated_data.pop('topics', [])
        post = Post.objects.create(**validated_data)
        post.category.set(categories)
        post.topics.set(topics)
        return post

    def update(self, instance, validated_data):
        categories = validated_data.pop('category', None)
        topics = validated_data.pop('topics', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if categories is not None:
            instance.category.set(categories)
        if topics is not None:
            instance.topics.set(topics)

        instance.save()
        return instance
