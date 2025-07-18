from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Post, PostImage, PostLike, PostScrap, Comment, CommentLike
from django.contrib.auth.models import User

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = PostImage
        fields = ['image',]

class PostSerializer(ModelSerializer):
    #읽기 전용 - 업로드된 이미지 리스트 반환용
    images = PostImageSerializer(many=True, read_only=True)
    #쓰기 전용 - 사용자가 업로드할 이미지들 받는 용도
    image_files = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    writer = serializers.ReadOnlyField(source = 'writer.username')
    comment_count = serializers.SerializerMethodField() #게시글의 댓글 개수
    like_count = serializers.SerializerMethodField() #게시글의 좋아요 개수

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'images', 'image_files', 'writer', 'comment_count', 'like_count']
    
    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_like_count(self, obj):
        return obj.likes.count()

    def validate_image_files(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("이미지는 최대 5장까지 업로드할 수 있습니다.")
        return value

    #PostImage객체 생성
    def create(self, validated_data):
        image_files = validated_data.pop('image_files', [])
        if len(image_files) > 5:
            raise serializers.ValidationError("이미지는 최대 5장까지 업로드할 수 있습니다.")

        post = Post.objects.create(**validated_data)

        for image in image_files:
            PostImage.objects.create(post=post, image=image)

        return post

class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = PostLike
        fields = ['id', 'post', 'user', 'created_at']

class PostScrapSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = PostScrap
        fields = ['id', 'post', 'user', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)  # 캐시된 좋아요 수
    user = serializers.ReadOnlyField(source='user.username')  # 댓글 작성자 이름
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'image', 'like_count', 'created_at', 'updated_at']

class CommentLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = CommentLike
        fields = ['id', 'comment', 'user', 'created_at']

