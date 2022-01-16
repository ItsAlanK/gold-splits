from django.contrib import admin
from .models import Post, Categories


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('date',)
    list_display = ('title', 'author')
    search_fields = ['title', 'content']


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name',]
