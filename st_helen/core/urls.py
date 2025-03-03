from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("quiz/", views.quiz, name="quiz" ),
    path("logout/", views.logout, name="logout"),
    path("settings/", views.settings, name="settings"),
    path("makepost", views.makepost, name="makepost"),
    path("like_post", views.likepost),
    path("connect/", views.connect, name="connect"),
    path("discover/", views.discover, name="discover")

]