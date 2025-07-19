from django.urls import path
from .views import QuestionListView, SubmitTestView, MyTestResultsView

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('submit/', SubmitTestView.as_view(), name='submit-test'),
    path('my-result/', MyTestResultsView.as_view(), name='my-result'),
]
