from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from django.urls import path, include
from .views import PostViewSet, CommentViewSet  

router = SimpleRouter(trailing_slash=False)
router.register('posts', PostViewSet, basename='post')

comments_router = routers.NestedSimpleRouter(router, 'posts', lookup='post')
comments_router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(comments_router.urls)),
]