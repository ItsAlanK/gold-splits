from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    """Model extends base form to take comments model"""
    class Meta:
        model = Comment
        fields = ('content',)


class PostForm(forms.ModelForm):
    """Model extends base form to take comments model"""
    class Meta:
        model = Post
        fields = ('title', 'hero_image', 'content', 'category',)
