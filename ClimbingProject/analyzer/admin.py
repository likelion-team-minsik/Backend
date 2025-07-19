from django.contrib import admin
from .models import Question, Choice, TestResult

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    inlines = [ChoiceInline]

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'result_type', 'created_at']