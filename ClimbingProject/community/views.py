from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from .models import Post, Comment, CommentLike, PostScrap
from .serializers import PostSerializer , CommentSerializer, CommentLikeSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

    #스크랩
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def scrap(self, request, pk=None):
        post = self.get_object()
        user = request.user
        scrap, created = PostScrap.objects.get_or_create(post=post, user=user)
        if created: #새로 스크랩
            return Response({'status': 'scrapped'}, status=status.HTTP_201_CREATED)
        else: #이미 스크랩 됨
            return Response({'status': 'already scrapped'}, status=status.HTTP_200_OK)

    #스크랩 취소
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unscrap(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            scrap = PostScrap.objects.get(post=post, user=user)
            scrap.delete()
            return Response({'status': 'unscrapped'}, status=status.HTTP_204_NO_CONTENT)
        except PostScrap.DoesNotExist:
            return Response({'status': 'not scrapped'}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] #비로그인자는 GET만 조회 가능

    def get_queryset(self, **kwargs):
        id = self.kwargs.get('post_pk')
        return self.queryset.filter(post_id=id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(user=self.request.user, post=post)

    #좋아요
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        like, created = CommentLike.objects.get_or_create(comment=comment, user=user)
        if created: #새로 좋아요
            comment.like_count = comment.likes.count()
            comment.save(update_fields=['like_count'])
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        else: #이미 좋아요 눌려있음
            return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

    #좋아요 취소
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        try:
            like = CommentLike.objects.get(comment=comment, user=user)
            like.delete()
            comment.like_count = comment.likes.count()
            comment.save(update_fields=['like_count'])
            return Response({'status': 'unliked'}, status=status.HTTP_204_NO_CONTENT)
        except CommentLike.DoesNotExist:
            return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)