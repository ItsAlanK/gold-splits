from django.test import TestCase
from .forms import ProfileForm


class TestProfileForm(TestCase):

    def test_profile_img_field_is_not_required(self):
        form = ProfileForm({'profile_img': ''})
        self.assertTrue(form.is_valid())

    def test_bio_field_is_not_required(self):
        form = ProfileForm({'bio': ''})
        self.assertTrue(form.is_valid())

    def test_fields_are_explicit_in_metaclass(self):
        form = ProfileForm()
        self.assertEqual(form.Meta.fields, ('profile_img', 'bio'))
