from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from django.db.models import Count, Q
from allauth.account.forms import SignupForm
from .models import Post, Comment, Category
from .forms import CommentForm, PostForm


class PostList(generic.ListView):
    """Post list which shows on home page"""
    model = Post
    queryset = Post.objects.annotate(
        q_count=Count('likes')).order_by('-q_count')[:7]
    template_name = 'pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.all()
        context["form"] = SignupForm
        return context


class AllPosts(generic.ListView):
    """List of all posts for Posts page"""
    model = Post
    queryset = Post.objects.order_by('-date')
    template_name = 'pages/posts.html'
    paginate_by = 8


class PostDetail(View):
    """Passes details of requested post"""
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.order_by('date')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        return render(
            request,
            "pages/post-management/post-page.html",
            {
                "post": post,
                "comments": comments,
                "comment_form": CommentForm(),
                "liked": liked,
            }
        )

    def post(self, request, slug, *args, **kwargs):
        """Checks liked to see if user has liked post,
        Takes comment form, adds details to comments model and
        redirects to post page."""
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.order_by('date')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post_page', args=[slug]))
        else:
            comment_form = CommentForm()
            return render(
                request,
                "pages/post-management/post-page.html",
                {
                    "post": post,
                    "comments": comments,
                    "comment_form": CommentForm(),
                    "liked": liked,
                }
            )

        return render(
            request,
            "pages/post-management/post-page.html",
            {
                "post": post,
                "comments": comments,
                "comment_form": CommentForm(),
                "liked": liked,
            }
        )


class AddLike(View):
    """Sets liked to true on post for current user and
    reloads page."""
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_page', args=[slug]))


class CreatePost(generic.CreateView):
    """Form view for user to create posts. Form takes
    title, hero image, category. Automatically sets slug and author"""
    model = Post
    template_name = 'pages/post-management/create-post.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.instance.slug = slugify(post_form.instance.title)
            post = post_form.save(commit=False)
            post.save()
        else:
            post_form = PostForm()

        return HttpResponseRedirect(
            reverse('post_page', args=[post_form.instance.slug]))


class EditPost(generic.UpdateView):
    """Form view to edit an existing post and load post."""
    model = Post
    template_name = 'pages/post-management/edit-post.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('post_page', kwargs={'slug': self.object.slug})


class DeletePost(generic.DeleteView):
    """Basic view to confirm delete post. Deletes post and
    redirects home."""
    model = Post
    template_name = 'pages/post-management/delete-post.html'

    def get_success_url(self):
        return reverse('home')


def category(request, name):
    """Function view to render category based on name."""
    category = Category.objects.get(name=name)
    posts = Post.objects.filter(category=category)
    return render(
        request, 'pages/category.html', {'name': name, 'posts': posts})


def search_results(request):
    """Takes request from search bar and queries posts
    by title and content to return matches"""
    if request.method == "POST":
        search = request.POST['search']
        results = Post.objects.filter(
            Q(title__icontains=search) | Q(content__icontains=search))
        return render(
            request, 'pages/search.html', {
                'search': search,
                'results': results,
            }
        )
    else:
        return render(
            request, 'pages/search.html', {}
        )
