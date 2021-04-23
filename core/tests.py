import datetime

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
    def setUp(self):
        self.user =  User.objects.create_superuser(
            username = 'Tester', 
            email = 'tester@admin.com', 
            password = 'password'
        )

    def test_featured_post_must_be_latest_one(self):
        """
        If there is not featured post, nothing will be displayed
        """
        create_post(user = self.user, featured = True, days = 3)
        latestFeaturedPost = create_post(user = self.user, featured = True, days = 2)
        response = self.client.get(reverse('core:home'))
        self.assertQuerysetEqual(
            response.context['featuredPost'],
            [latestFeaturedPost]
        )

    def test_tags(self):
        pass
        