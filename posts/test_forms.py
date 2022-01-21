from django.test import TestCase
from .forms import PostForm, CommentForm


class TestPostForm(TestCase):

    def test_fields_are_explicit_in_metaclass(self):
        form = PostForm()
        self.assertEqual(form.Meta.fields,
                         ('title', 'hero_image', 'content', 'category',))

    def test_title_field_is_required(self):
        form = PostForm({'title': ''})
        self.assertFalse(form.is_valid())

    def test_content_field_is_required(self):
        form = PostForm({'content': ''})
        self.assertFalse(form.is_valid())


class TestCommentForm(TestCase):

    def test_fields_are_explicit_in_metaclass(self):
        form = CommentForm()
        self.assertEqual(form.Meta.fields,
                         ('content',))

    def test_content_field_is_required(self):
        form = CommentForm({'content': ''})
        self.assertFalse(form.is_valid())
