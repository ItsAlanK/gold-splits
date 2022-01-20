from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Sets sorting and filtering params for profile"""
    list_filter = ('user',)
    list_display = ('user',)
