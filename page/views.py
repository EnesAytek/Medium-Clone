from django.shortcuts import render
from blog.models import Post, Tag, Category

def home_view(request):
    posts = Post.objects.filter(is_active=True)
    top_posts = posts.order_by('-view_count')[:6]
    tags = Tag.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    context = dict(
        posts=posts,
        tags=tags,
        categories=categories,
        top_posts=top_posts
    )
    return render(request, 'page/home_page.html', context)