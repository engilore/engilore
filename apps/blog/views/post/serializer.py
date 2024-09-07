from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 
            'title', 
            'slug', 
            'content', 
            'author', 
            'status', 
            'created_at', 
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'author']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        if not request.user.is_admin and instance.author != request.user:
            raise serializers.ValidationError("You do not have permission to edit this post.")
        return super().update(instance, validated_data)
