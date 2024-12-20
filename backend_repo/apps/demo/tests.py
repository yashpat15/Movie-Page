from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment

class PostListViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        post = Post.objects.create(text="Test post", user=user)
        Comment.objects.create(text="Test comment 1", post=post, user=user)
        Comment.objects.create(text="Test comment 2", post=post, user=user)

    def test_post_list_view(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('post_text', response.json()['results'][0])
