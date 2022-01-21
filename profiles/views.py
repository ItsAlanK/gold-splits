from django.views import generic, View
from django.shortcuts import reverse, get_object_or_404, render
from django.contrib.auth.models import User
from .models import Profile
from posts.models import Post
from .forms import ProfileForm


class EditProfile(generic.UpdateView):
    """Creates updateview to allow users to edit
    their profile bio and image"""
    model = Profile
    template_name = 'pages/profile/edit-profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse('home')


class ProfileView(View):
    """View to display user profiles and
    list posts related to the user"""
    def get(self, request, name, *args, **kwargs):
        user_id = User.objects.get(username=name).pk
        profile = get_object_or_404(Profile, user=user_id)
        posts = Post.objects.filter(author=profile.user)

        return render(
            request,
            "pages/profile/profile-page.html",
            {
                "profile": profile,
                "posts": posts
            }
        )
