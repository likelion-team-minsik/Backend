from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Question, Answer
from django.contrib.auth.models import User

class QuestionSerializer(ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Question
        fields = ['id', 'title', 'created_at', 'user']

class AnswerSerializer(ModelSerializer):
    responder = serializers.ReadOnlyField(source='responder.username')

    class Meta:
        model = Answer
        fields = ['id', 'question', 'responder', 'content', 'created_at']