from django.shortcuts import render
from rest_framework import generics, filters
from community.models import Post
from community.serializers import PostSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
from .serializers import HighlightPostSerializer 

class PostSearchView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields   = ['title', 'content']   

class PostSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        keyword = request.query_params.get('q', '').strip()
        qs = Post.objects.none()

        if keyword:
            qs = Post.objects.filter(
                Q(title__icontains=keyword) | Q(content__icontains=keyword)
            ).order_by('-created_at')

        data = HighlightPostSerializer(qs, many=True, context={'keyword': keyword}).data
        return Response(data)