from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from .models import Post, Comment
from allauth.account.forms import LoginForm, SignupForm
from .forms import CommentForm, PostForm


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
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "pages/post-page.html",
            {
                "post": post,
                "comments": comments,
                "comment_form": CommentForm(),
                "liked": liked,
            }
        )

    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.order_by('date')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "pages/post-page.html",
            {
                "post": post,
                "comments": comments,
                "comment_form": CommentForm(),
                "liked": liked,
            }
        )


class AddLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_page', args=[slug]))


class CreatePost(View):

    def get(self, request, *args, **kwargs):

        return render(
            request,
            "pages/create-post.html",
            {
                "post_form": PostForm(),
            }
        )

    def post(self, request, *args, **kwargs):
        post_form = PostForm(data=request.POST)

        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.instance.slug = slugify(post_form.instance.title)
            post = post_form.save(commit=False)
            post.save()
        else:
            post_form = PostForm()

        return HttpResponseRedirect(reverse('post_page', args=[post_form.instance.slug]))
