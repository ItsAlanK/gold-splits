from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """Model extends base form to take comments model"""
    class Meta:
        model = Comment
        fields = ('content',)