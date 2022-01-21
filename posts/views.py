from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.utils.text import slugify
from .models import Post, Comment, Category
from django.db.models import Count, Q
from allauth.account.forms import LoginForm, SignupForm
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
            "pages/post-management/post-page.html",
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


class CreatePost(generic.CreateView):
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
    model = Post
    template_name = 'pages/post-management/edit-post.html'
    form_class = PostForm

    def get_success_url(self):
        return reverse('post_page', kwargs={'slug': self.object.slug})


class DeletePost(generic.DeleteView):
    model = Post
    template_name = 'pages/post-management/delete-post.html'

    def get_success_url(self):
        return reverse('home')


def category(request, name):
    category = Category.objects.get(name=name)
    posts = Post.objects.filter(category=category)
    return render(
        request, 'pages/category.html', {'name': name, 'posts': posts})


def search_results(request):
    if request.method == "POST":
        search = request.POST['search']
        results = Post.objects.filter(
            Q(title__icontains=search) | Q(content__icontains=search))
        category = Category.objects.all()
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
