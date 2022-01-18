from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post, Comment
from allauth.account.forms import LoginForm, SignupForm
from .forms import CommentForm


class PostList(generic.ListView):
    """Post list which shows on home page"""
    model = Post
    queryset = Post.objects.order_by('-date')
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.all()
        return context


class AllPosts(generic.ListView):
    """List of all posts for Posts page"""
    model = Post
    queryset = Post.objects.order_by('-date')
    template_name = 'pages/posts.html'
    paginate_by = 10


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.order_by('date')

        return render(
            request,
            "pages/post-page.html",
            {
                "post": post,
                "comments": comments,
                "Comment_form": CommentForm(),
            }
        )
