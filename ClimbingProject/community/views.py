from rest_framework.viewsets import ModelViewSet
from .models import Post, Comment, CommentLike, PostScrap
from .serializers import PostSerializer , CommentSerializer, CommentLikeSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(writer = self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        like, created = CommentLike.objects.get_or_create(comment=comment, user=user)
        if created:
            comment.like_count = comment.likes.count()
            comment.save(update_fields=['like_count'])
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'already liked'}, status=status.HTTP_200_OK)

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

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def scrap(self, request, pk=None):
        post = self.get_object()
        user = request.user
        scrap, created = PostScrap.objects.get_or_create(post=post, user=user)
        if created:
            return Response({'status': 'scrapped'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'already scrapped'}, status=status.HTTP_200_OK)

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