from django.urls import path
from .views import PostSearchView, CommentedPostSearchView
from .views import PublicSearchView

urlpatterns = [
    path('', PostSearchView.as_view(), name='post-search'), 
    path('commented/search/', CommentedPostSearchView.as_view(), name='commented-post-search'), 
    path('posts/search/', PublicSearchView.as_view(), name='public-post-search'),
]