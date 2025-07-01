from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User

#커뮤니티 게시글
class Post(models.Model):
    title = models.CharField(verbose_name="제목", max_length=100)
    content = models.TextField(verbose_name="내용")
    image = models.ImageField(verbose_name="이미지", upload_to='community/images/', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="작성일", auto_now_add=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True) 
    
    def __str__(self):
        return self.title

#커뮤니티 게시글 좋아요
class PostLike(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user') #유저 게시글에 좋아요 한 개만 가능

#게시글 댓글
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') #어떤 게시글에 달린 댓글인지
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 댓글 작성자
    content = models.TextField(verbose_name="댓글 내용")
    image = models.ImageField(verbose_name="댓글_이미지", upload_to='comments/images/', null=True, blank=True)  # 이미지 첨부 (선택사항)
    created_at = models.DateTimeField(verbose_name="댓글_작성일", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="댓글_수정일", auto_now=True)
    like_count = models.PositiveIntegerField(verbose_name="좋아요 수", default=0)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'

#댓글의 좋아요
class CommentLike(models.Model):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')  # 한 유저가 같은 댓글에 중복 좋아요 방지

    def __str__(self):
        return f'{self.user.username} likes comment {self.comment.id}'

#게시글 스크랩
class PostScrap(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='scraps')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')  # 중복 스크랩 방지

    def __str__(self):
        return f'{self.user.username} scrapped post {self.post.title}'