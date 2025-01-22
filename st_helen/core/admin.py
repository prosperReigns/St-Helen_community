from django.contrib import admin
from .models import Profile,Posts,LikePost,Question, Option

# Register your models here.
admin.site.register(Profile)
admin.site.register(Posts)
admin.site.register(LikePost)
admin.site.register(Question)
admin.site.register(Option)