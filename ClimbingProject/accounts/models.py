from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    full_name = models.CharField(max_length=50, blank=True)
    #마이페이지 정보수정
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    nickname = models.CharField(max_length=30, blank=True)