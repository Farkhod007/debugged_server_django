import datetime
import pprint

from django.contrib.auth.models import User
from django.test.client import Client
from core.models.post import Post
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

def create_post(user, featured, days):
    return Post.objects.create(
        user = user, 
        title = "New post",
        body = "This is a body text",
        image = "posts/post-1_HWfiOph.png",
        excerpt = "This is a excerpt",
        featured = featured,
        status = "PB",
        created_at = timezone.now() - datetime.timedelta(days = days)
    )

class HomeViewTests(TestCase):
    def get_user(self):
        return User.objects.create_superuser(
            username = 'Tester', 
            email = 'tester@admin.com', 
            password = 'password'
        )

    def test_featured_post_must_be_latest_one(self):
        """
        If there is not featured post, nothing will be displayed
        """
        user = self.get_user()
        create_post(user = user, featured = True, days = 3)
        post = create_post(user = user, featured = True, days = 2)
        response = self.client.get(reverse('core:home'))
        self.assertQuerysetEqual(
            response.context['feturedPost'],
            [post]
        )
        