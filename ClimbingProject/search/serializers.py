from community.serializers import PostSerializer
import re
from rest_framework import serializers
from community.models import Post

class HighlightPostSerializer(serializers.ModelSerializer):
    highlighted_title   = serializers.SerializerMethodField()
    highlighted_content = serializers.SerializerMethodField()

    class Meta:
        model  = Post
        fields = ['id', 'highlighted_title', 'highlighted_content', 'created_at']

    #하이라이트
    def _highlight(self, text, keyword):
        """
        keyword(대소문자 무시)가 text에 있을 때 <mark>…</mark> 로 감싸서 반환
        """
        if not keyword:
            return text
        
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        return pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)

    def get_highlighted_title(self, obj):
        keyword = self.context.get('keyword', '')
        return self._highlight(obj.title, keyword)

    def get_highlighted_content(self, obj):
        keyword = self.context.get('keyword', '')
        return self._highlight(obj.content, keyword)
