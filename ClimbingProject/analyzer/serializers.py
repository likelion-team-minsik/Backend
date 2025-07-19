from rest_framework import serializers
from .models import Question, Choice, TestResult

# ChoiceSerializer: 선택지 하나에 대한 정보
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'type', 'score']
        read_only_fields = ['id', 'text', 'type', 'score']

# QuestionSerializer: 질문 + 연결된 선택지
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']


# 결과 저장용 시리얼라이저 (선택사항)
class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id', 'user', 'result_type', 'scores', 'created_at']