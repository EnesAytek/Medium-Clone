from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostModelForm
from .models import Category, Tag, Post, UserPostFav
import json





@login_required(login_url='user:login_view')
def fav_update(request):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=request.POST.get('slug'))
        if post:
            post_fav, created = UserPostFav.objects.get_or_create(
                user=request.user,
                post=post,
            )
            if not created:
                post_fav.is_deleted = not post_fav.is_deleted
                post_fav.save()
    return JsonResponse({"status":"OK"})


@login_required(login_url='user:login_view')
def create_blog_post_view(request):
    title = 'Yeni Blog Post :'
    form = PostModelForm()
    
    if request.method == 'POST':
        form = PostModelForm(request.POST or None, request.FILES or None )
     
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            tags = json.loads(form.cleaned_data.get('tag'))
            for tag in tags:
                tag, created = Tag.objects.get_or_create(title=tag.get('value').lower())
                tag.is_active = True
                tag.save()
                f.tag.add(tag)
            messages.success(request,'Gönderi Kaydedildi')
            return redirect('home_view')
     
    return render(request, 'common_components/form.html', context={'form':form,'title':title})


def category_view(request,category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category) 
    context = dict(
        category=category,
        posts=posts,
    )
    return render(request, 'blog/post_list.html', context)


def tag_view(request,tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tag=tag)
    context = dict(
        tag=tag,
        posts=posts,
    )
    return render(request, 'blog/post_list.html', context)


@login_required(login_url='user:login_view')
def post_edit_view(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if not post.user == request.user:
        messages.warning(request, 'Bu postu düzenleyemezsin')
        return redirect('home_view')
    title = post.title
    form = PostModelForm(instance=post)
    
    if request.method == 'POST':
        form = PostModelForm(request.POST or None, request.FILES or None, instance=post )
     
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            tags = json.loads(form.cleaned_data.get('tag'))
            for tag in tags:
                tag, created = Tag.objects.get_or_create(title=tag.get('value').lower())
                tag.is_active = True
                tag.save()
                f.tag.add(tag)
            messages.success(request,'Postunuz Düzenlendi')
            return redirect('home_view')
    
    context = dict(
        title=title,
        form=form,
        
        )
    return render(request, 'common_components/form.html', context)