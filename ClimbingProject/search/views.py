from django.shortcuts import render
from rest_framework import generics, filters
from community.models import Post
from community.serializers import PostSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .serializers import HighlightPostSerializer 
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

class PostSearchView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        user = request.user
        keyword = request.query_params.get('q', '').strip()
        qs = Post.objects.none()

        if keyword:
            qs = Post.objects.filter(
                Q(writer=user),
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            ).order_by('-created_at')

        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)
    
class CommentedPostSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        keyword = request.query_params.get('q', '').strip()
        qs = Post.objects.filter(comments__user=user).distinct().order_by('-created_at')

        if keyword:
            qs = qs.filter(
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            )

        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)
    
class PublicSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        keyword = request.query_params.get('q', '').strip()

        if not keyword:  
            return Response([])

        qs = Post.objects.filter(
            Q(title__icontains=keyword) | Q(content__icontains=keyword)
        ).order_by('-created_at')

        serializer = PostSerializer(qs, many=True)
        return Response(serializer.data)