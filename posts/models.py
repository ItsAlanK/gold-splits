from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    """Model holding category names
    can only be created or removed by admins
    """
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Model containing all data relating to posts."""
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True)
    content = RichTextUploadingField()
    hero_image = models.FileField(
        upload_to="media/", blank=True, default='placeholder')
    likes = models.ManyToManyField(User, related_name="likes", blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT,
        default="General", related_name="posts")

    class Meta:
        """Sorts model in descending order by date created."""
        ordering = ['-date']

    def __str__(self):
        return self.title

    def number_of_likes(self):
        """Counts number of likes on post."""
        return self.likes.count()


class Comment(models.Model):
    """Model containing comment data"""
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Sorts model in descending order by date created."""
        ordering = ['date']

    def __str__(self):
        return f"Comment: {self.content} Written by: {self.user}"
