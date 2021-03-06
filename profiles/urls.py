from django.urls import path
from . import views


urlpatterns = [
    path(
        'edit-profile/<int:pk>', views.EditProfile.as_view(),
        name='edit_profile'
        ),
    path(
        'profile/<str:name>', views.ProfileView.as_view(),
        name="profile_page"
        ),
]
