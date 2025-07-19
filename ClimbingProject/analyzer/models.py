from django.db import models
from django.conf import settings
# Create your models here.

#질문
class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

#선택
class Choice(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    type = models.CharField(max_length=20)
    score = models.IntegerField()

#결과 저장
class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    result_type = models.CharField(max_length=20) # 예: '도전형'
    scores = models.JSONField()  # {"재미형": 14, "계획형": 11, ...}
    created_at = models.DateTimeField(auto_now_add=True)