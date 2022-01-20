from .models import Profile
from django.views import generic
from django.shortcuts import reverse
from .forms import ProfileForm


class EditProfile(generic.UpdateView):
    model = Profile
    template_name = 'pages/edit-profile.html'
    form_class = ProfileForm

    def get_success_url(self):
        return reverse('home')
