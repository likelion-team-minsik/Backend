from django.urls import path
from .views import PostSearchView, CommentedPostSearchView

urlpatterns = [
    path('', PostSearchView.as_view(), name='post-search'), 
    path('commented/search/', CommentedPostSearchView.as_view(), name='commented-post-search'), 
]