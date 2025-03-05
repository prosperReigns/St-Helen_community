from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("quiz/", views.quiz, name="quiz" ),
    path("logout/", views.logout, name="logout"),
    path("settings/", views.settings, name="settings"),
    path("makepost/", views.makepost, name="makepost"),
    path("like_post/", views.likepost, name="likepost"),
    path("connect/", views.connect, name="connect"),
    path("discover/", views.discover, name="discover"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)