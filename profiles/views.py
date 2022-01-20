from .models import Profile
from django.views import generic, View
from django.shortcuts import reverse, get_object_or_404, render
from .forms import ProfileForm


class EditProfile(generic.UpdateView):
    model = Profile
    template_name = 'pages/profile/edit-profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse('home')


class ProfileView(View):

    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)

        return render(
            request,
            "pages/profile/profile-page.html",
            {
                "profile": profile,
            }
        )
