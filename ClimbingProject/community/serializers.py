from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Post, Comment, CommentLike, PostScrap
from django.contrib.auth.models import User

class PostSerializer(ModelSerializer):
    writer = serializers.ReadOnlyField(source = 'writer.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'writer']

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)  # 캐시된 좋아요 수
    user = serializers.ReadOnlyField(source='user.username')  # 댓글 작성자 이름

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'image', 'created_at', 'updated_at', 'like_count']


class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CommentLike
        fields = ['id', 'comment', 'user', 'created_at']

class PostScrapSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = PostScrap
        fields = ['id', 'post', 'user', 'created_at']