from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from django.urls import path, include
from .views import PostViewSet, CommentViewSet  

posts_router = SimpleRouter(trailing_slash=False)
posts_router.register('posts', PostViewSet, basename='post')

comments_router = routers.NestedSimpleRouter(posts_router, 'posts', lookup='post')
comments_router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(posts_router.urls)),
    path('', include(comments_router.urls)),
]