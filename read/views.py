from django.shortcuts import render,get_object_or_404
from blog.models import Post
from user_profile.models import Profile


def all_post_view(request, user_slug):
    profile = get_object_or_404(Profile, slug=user_slug)
    posts = Post.objects.filter(user=profile.user, is_active=True)
    context = dict(
        profile=profile,
        posts=posts,
    )
    return render(request, 'read/all_post.html', context)


def post_detail(request, user_slug, post_slug):
    post = get_object_or_404(Post, slug=post_slug, is_active=True)
    post.view_count += 1
    post.save()
    context = dict(
        post=post,   
    )
    return render(request, 'read/post_detail.html', context)