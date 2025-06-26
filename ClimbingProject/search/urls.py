from django.urls import path
from .views import PostSearchView

urlpatterns = [
    path('', PostSearchView.as_view(), name='post-search'),  
]