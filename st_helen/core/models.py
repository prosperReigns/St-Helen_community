from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile_image.png')
    location = models.CharField(max_length=100, blank=True)