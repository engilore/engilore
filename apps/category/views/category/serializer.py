from rest_framework import serializers
from category.models import Category
from category.views.topic.view import TopicSerializer


class CategorySerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'topics']
