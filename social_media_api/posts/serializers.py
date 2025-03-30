from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        related_only_fields = ['author']
        
    def get_comment_count(self, obj):
        return Comment.objects.filter(post=obj).count()

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post_title = serializers.ReadOnlyField(source='post.title')
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'post_title', 'content', 'created_at', 'updated_at']
