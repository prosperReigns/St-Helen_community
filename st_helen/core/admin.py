from django.contrib import admin
from .models import LikePost, Question, Option, Post, Response, Profile

# Register your models here.
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Response)
admin.site.register(Profile)