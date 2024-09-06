from django.contrib import admin
from .models import Profile,Posts,LikePost

# Register your models here.
admin.site.register(Profile)
admin.site.register(Posts)
admin.site.register(LikePost)