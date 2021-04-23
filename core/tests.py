import datetime

from django.contrib.auth.models import User
from django.test.client import Client
from core.models.post import Post
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

def create_post(user, title, featured, days):
    post = Post.objects.create(
        user = user, 
        title = title,
        body = "This is a body text",
        image = "posts/post-1_HWfiOph.png",
        excerpt = "This is a excerpt",
        featured = featured,
        status = "PB"
    )
    Post.objects.filter(
        pk = post.pk
    ).update(created_at = timezone.now() + datetime.timedelta(days = days))
    return post


class HomeViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
            username = 'Tester', 
            email = 'tester@admin.com', 
            password = 'password'
        )

    def test_featured_post_must_be_latest_one(self):
        """
        If there is more than one featured post, must get the latest one
        """
        create_post(
            user = self.user,
            title = "Older post", 
            featured = True, 
            days = -3
        )
        post = create_post(
            user = self.user, 
            title = "Newer post",
            featured = True, 
            days = -2
        )
        response = self.client.get(reverse('core:home'))
        self.assertEqual(
            response.context['featuredPost'],
            post
        )
    

    def test_if_there_is_no_featured_post_nothing_will_be_displayed(self):
        """
        If there is no featured post, nothing will be displayed
        """
        response = self.client.get(reverse('core:home'))
        self.assertIsNone(response.context['featuredPost'])
        self.assertNotContains(response, "blogpost featured")


    def test_featured_post_must_be_posted_in_the_past(self):
        """
        Featured post must be posted in the past
        """
        pastPost = create_post(
            user = self.user, 
            title = "Past post",
            featured = True, 
            days = -3
        )
        create_post(
            user = self.user, 
            title = "Future post",
            featured = True, 
            days = 3
        )
        response = self.client.get(reverse('core:home'))
        self.assertEqual(
            response.context['featuredPost'],
            pastPost
        )


    def test_regular_posts_was_ordered_in_descending_by_created_at(self):
        """
        Regular posts must be ordered in decending by created at field
        """
        firstPost = create_post(
            user = self.user, 
            title = "First post",
            featured = False, 
            days = -3
        )
        secondPost = create_post(
            user = self.user, 
            title = "Second post",
            featured = False, 
            days = -2
        )
        response = self.client.get(reverse('core:home'))
        self.assertQuerysetEqual(
            response.context['regularPosts'],
            [repr(secondPost), repr(firstPost)]
        )
    

    def test_if_there_are_no_regular_posts_nothing_will_be_displayed(self):
        """
        If there is no regular post, nothing will be displayed
        """
        response = self.client.get(reverse('core:home'))
        self.assertQuerysetEqual(response.context['regularPosts'], [])
        self.assertNotContains(response, "normal")


    def test_regular_posts_must_be_posted_in_the_past(self):
        """
        Regular posts must be posted in the past
        """
        pastPost = create_post(
            user = self.user, 
            title = "Past post",
            featured = False, 
            days = -3
        )
        create_post(
            user = self.user, 
            title = "Future post",
            featured = False, 
            days = 3
        )
        response = self.client.get(reverse('core:home'))
        self.assertQuerysetEqual(
            response.context['regularPosts'],
            [repr(pastPost)]
        )