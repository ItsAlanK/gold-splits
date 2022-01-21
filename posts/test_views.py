from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Category, Post

class TestViews(TestCase):

    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/index.html')

    def test_get_all_posts_page(self):
        response = self.client.get('/posts')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/posts.html')

    def test_get_category_page(self):
        category = Category.objects.create(name='General')
        response = self.client.get(f'/category/{category.name}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category.html')

    def test_get_post_detail_page(self):
        author = User.objects.create(username='Alan')
        category = Category.objects.create(name='General')
        post = Post.objects.create(title='test', category=category, author=author)
        slug = slugify(post.title)
        response = self.client.get(f'/{slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'pages/post-management/post-page.html')
