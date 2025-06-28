from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views
from .views import UserProfileView


user_router = SimpleRouter()
user_router.register('user',views.UserViewSet)

urlpatterns = [
    path('',include(user_router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]

