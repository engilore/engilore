from rest_framework import serializers
from category.models import Topic, Category


class TopicSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'category']