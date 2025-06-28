from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User

class Question (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #질문자(사용자)
    title = models.CharField(verbose_name="질문제목", max_length=200)
    created_at = models.DateTimeField(verbose_name="질문_작성일", auto_now_add=True)
    is_answered = models.BooleanField(default=False)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers') #이 답변이 달린 질문
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) #답변자(관리자)
    content = models.TextField(verbose_name="답변내용")
    created_at = models.DateTimeField(verbose_name="답변_작성일", auto_now_add=True)