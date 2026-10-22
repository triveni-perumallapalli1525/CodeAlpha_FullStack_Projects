
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("register/", views.register_view, name="register"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="social/login.html"
        ),
        name="login",
    ),

    path("create-post/", views.create_post, name="create_post"),

    path("like/<int:post_id>/", views.like_post, name="like_post"),

    path("comment/<int:post_id>/", views.add_comment, name="add_comment"),

    path("profile/<str:username>/", views.profile_view, name="profile"),

    path("follow/<str:username>/", views.follow_user, name="follow_user"),

    path("logout/", views.logout_view, name="logout"),
]
