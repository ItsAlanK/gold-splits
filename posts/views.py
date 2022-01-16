from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostList(ListView):
    model = Post
    queryset = Post.objects.order_by('-date')
    template_name = 'pages/index.html'
