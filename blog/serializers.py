from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'content', 'publish', 'created_at', 'updated_at', 'status', 'image', 'meta_description']
        read_only_fields = ['id', 'created_at', 'updated_at']
