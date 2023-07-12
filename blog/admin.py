from django.contrib import admin
from .models import Category, Post, Tag, UserPostFav


@admin.register(UserPostFav)
class UserPostFavAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user', 
        'post',
        'is_deleted'
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title', 
        'is_active'
    ]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title', 
        'is_active'
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title', 
        'is_active',
        'view_count'
    ]
