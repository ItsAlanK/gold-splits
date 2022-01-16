from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('date',)
    list_display = ('title', 'author')
    search_fields = ['title', 'content']


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'content', 'post')
    search_fields = ['user', 'content', 'post', 'date']
