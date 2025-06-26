from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import QuestionViewSet, AnswerViewSet

router = SimpleRouter(trailing_slash=False)
router.register('questions', QuestionViewSet, basename='question')
router.register('answers', AnswerViewSet, basename='answer')

urlpatterns = [
    path('', include(router.urls)),
]