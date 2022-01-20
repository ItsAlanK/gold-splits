from .models import Profile
from django import forms


class ProfileForm(forms.ModelForm):
    """Model extends base form to take comments model"""
    class Meta:
        model = Profile
        fields = ('profile_img', 'bio',)
