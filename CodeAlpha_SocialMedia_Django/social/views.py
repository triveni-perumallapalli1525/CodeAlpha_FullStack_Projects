
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .models import Profile, Post, Comment, Like, Follow


def home(request):
    posts = Post.objects.select_related("author").prefetch_related(
        "likes", "comments"
    )
    return render(request, "social/home.html", {"posts": posts})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "social/register.html", {"form": form})


@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        image_url = request.POST.get("image_url", "").strip()

        if content:
            Post.objects.create(
                author=request.user,
                content=content,
                image_url=image_url,
            )
            messages.success(request, "Post published!")
        else:
            messages.error(request, "Please write something before posting.")

    return redirect("home")


@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(
        post=post, user=request.user
    )
    if not created:
        like.delete()
    return redirect(request.POST.get("next") or "home")


@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get("content", "").strip()

    if content:
        Comment.objects.create(
            post=post, author=request.user, content=content
        )
    return redirect(request.POST.get("next") or "home")


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=profile_user)

    if request.method == "POST" and request.user == profile_user:
        profile.bio = request.POST.get("bio", "").strip()
        profile.profile_picture = request.POST.get(
            "profile_picture", ""
        ).strip()
        profile.save()
        messages.success(request, "Profile updated!")

    posts = Post.objects.filter(author=profile_user)
    is_following = Follow.objects.filter(
        follower=request.user, following=profile_user
    ).exists()

    return render(request, "social/profile.html", {
        "profile_user": profile_user,
        "profile": profile,
        "posts": posts,
        "is_following": is_following,
        "followers_count": Follow.objects.filter(
            following=profile_user
        ).count(),
        "following_count": Follow.objects.filter(
            follower=profile_user
        ).count(),
    })


@login_required
@require_POST
def follow_user(request, username):
    target = get_object_or_404(User, username=username)

    if target != request.user:
        follow, created = Follow.objects.get_or_create(
            follower=request.user, following=target
        )
        if not created:
            follow.delete()

    return redirect("profile", username=username)


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("home")
