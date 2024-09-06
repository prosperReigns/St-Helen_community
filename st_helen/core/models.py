from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

# Create your models here.

User = get_user_model()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile_image.png')
    location = models.CharField(max_length=100, blank=True)

class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) #keep track of number of posts 
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to="post_images")
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

class LikePost(models.Model): 
    post_id = models.CharField(max_length=100) #keep track of which posts are being liked 
    username = models.CharField(max_length=100) #keep track of who is liking the post

class FollowerCount(models.Model): 
    followers = models.CharField(max_length=100)
    user = models.CharField(max_length=100)