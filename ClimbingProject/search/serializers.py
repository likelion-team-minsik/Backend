from community.serializers import PostSerializer
import re
from rest_framework import serializers
from community.models import Post

class HighlightPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at']