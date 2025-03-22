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
        return f"{self.user} made a post {self.id}"
    
class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # this is the correct definition
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} liked {self.post}"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #gets the user logged in
    bio = models.TextField(blank=True) #each profile should contain a bio
    profileimg = models.ImageField(upload_to='profile_images', default='blank_profile_image.png') #default profile image is blank

    YEAR_GROUP_CHOICES = [
        ('7', 'Year 7'),
        ('8', 'Year 8'),
        ('9', 'Year 9'),
        ('10', 'Year 10'),
        ('11', 'Year 11'),
        ('12', 'Year 12'),
        ('13', 'Year 13'),
    ] #tuple to give a drop down list of year group choices, as per Django's language 

    year_group = models.CharField(max_length=7, choices=YEAR_GROUP_CHOICES, blank=True, null=True)
    #each profile should have the students actual year group/ a null value if not set 

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
    
class Club (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4) #gives each club a unique ID and makes this the primary key
    club_name = models.CharField(max_length=100) #each club has a unique name (validation should exist in the view)
    image = models.ImageField(upload_to='club_profile_images', default='blank_club_profile_image.png')
    description = models.TextField(blank=True,  max_length=300) #each club should have a description
    
    CLUB_CATEGORIES = [
        ('Academic', 'Academic & Professional'),
        ('Sport', 'Sports & Recreation'),
        ('Arts', 'Arts & Creativity'),
        ('Identity', 'Culture & Identity Based'),
        ('Community', 'Community Service & Social Impact'),
        ('Interests', 'Special Interests & Hobbies'),
        ('Other', 'Other')
    ]

    club_category = models.CharField(choices=CLUB_CATEGORIES, max_length=30, blank=True, null=True) #each club has a category 

    def __str__(self):
        return self.club_name #returns the club name 