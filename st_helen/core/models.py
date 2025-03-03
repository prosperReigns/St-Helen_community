from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.contrib.auth.models import User

User = get_user_model()

# Create your models here.
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) #gives each post unique ID and makes this the primary key
    created_at = models.DateTimeField(default=datetime.now) #gives post a time created so they can be ordered
    image = models.ImageField(upload_to='post_images')
    caption = models.CharField(max_length=1500) #caption is validated by number of characters 
    no_of_likes = models.IntegerField(default=0) 
    user = models.ForeignKey(User, on_delete=models.CASCADE) #each post allocated to a user

    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    user = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} liked {self.post_id}"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Question(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    question = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.question #returns a string representation of any object in the Questions model

class Option(models.Model):
    created_at = models.DateTimeField(default=datetime.now)
    option = models.CharField(max_length=200, blank=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options") #creates one to many relationship with questions to options 

    def __str__(self):
        return self.option

class Response(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, null=True, default=None) #signifies a many to one relationship (many responses can be tied to one user)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.student} answered '{self.option}' to '{self.question}'" #gives a string answer displaying the user and the response to a question

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user}"