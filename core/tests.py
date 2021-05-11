import datetime

from django.contrib.auth.models import User
from django.test.client import Client
from core.models.post import Post
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from core.models.category import Category

def create_post(user, title, featured, days, status = 'PB'):
    post = Post.objects.create(
        user = user, 
        title = title,
        body = "This is a body text",
        image = "posts/post-1_HWfiOph.png",
        excerpt = "This is a excerpt", 
        featured = featured,
        status = status
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
        self.assertNotContains(response, 'class="blogpost featured"')


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

    
    def test_featured_post_featured_field_must_be_equal_to_true(self):
        """
        Featured post's featured field value must be eqaul to true
        """
        featuredPost = create_post(
            user = self.user, 
            title = "Featured post",
            featured = True, 
            days = -3
        )
        create_post(
            user = self.user, 
            title = "Not featured post",
            featured = False, 
            days = -2
        )
        response = self.client.get(reverse('core:home'))
        self.assertEqual(
            response.context['featuredPost'],
            featuredPost
        )


    def test_featured_post_status_must_be_equal_to_published(self):
        """
        Featured post's status field must be eqaul to published
        """
        publishedPost = create_post(
            user = self.user, 
            title = "Published post",
            featured = True, 
            days = -3,
            status = 'PB'
        )
        create_post(
            user = self.user, 
            title = "Pending post",
            featured = True, 
            days = -2,
            status = 'PN'
        )
        response = self.client.get(reverse('core:home'))
        self.assertEqual(
            response.context['featuredPost'],
            publishedPost
        )


    def test_regular_post_was_ordered_in_descending_by_created_at(self):
        """
        Regular post must be ordered in decending by created at field
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
    

    def test_if_there_is_no_regular_post_nothing_will_be_displayed(self):
        """
        If there is no regular post, nothing will be displayed
        """
        response = self.client.get(reverse('core:home'))
        self.assertQuerysetEqual(response.context['regularPosts'], [])
        self.assertNotContains(response, 'class="normal"')


    def test_regular_post_must_be_posted_in_the_past(self):
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

    
    def test_regular_post_featured_field_must_be_equal_to_true(self):
        """
        Regular post's featured field value must be eqaul to true
        """
        regularPost = create_post(
            user = self.user, 
            title = "Regular post",
            featured = False, 
            days = -3
        )
        create_post(
            user = self.user, 
            title = "Featured post",
            featured = True, 
            days = -2
        )
        response = self.client.get(reverse('core:home'))
        self.assertQuerysetEqual(
            response.context['regularPosts'],
            [repr(regularPost)]
        )


    def test_regular_post_status_must_be_equal_to_published(self):
        """
        Featured post's status field must be eqaul to published
        """
        publishedPost = create_post(
            user = self.user, 
            title = "Published post",
            featured = False, 
            days = -3,
            status = 'PB'
        )
        create_post(
            user = self.user, 
            title = "Pending post",
            featured = False, 
            days = -2,
            status = 'PN'
        )
        response = self.client.get(reverse('core:home'))
        self.assertQuerysetEqual(
            response.context['regularPosts'],
            [repr(publishedPost)]
        )

def create_category(name, days):
        
        time = timezone.now() + datetime.datetime(days = days) 
        return Category.objects.create(name = name, created_at = time)




class Testcategoryview(TestCase):
    
    def test_was_published_recently_with_future_category(self):
        
        time = timezone.now() + datetime.datetime(days=1, second=1) 
        future_category = Category(created_at = time)
        self.assertIs(future_category.was_published_recently(), True)

    
    def test_no_category(self):
        """
        If no category exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('core:category'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No category are available.")
        self.assertQuerysetEqual(response.context['posts'], [])

    
    
    def test_future_category_and_past_category(self):
        """
        Even if both past and future category exist, only past category
        are displayed.
        """
        category = create_category(name = "Past category.", days=-30)
        create_category(name="Future category.", days=30)
        response = self.client.get(reverse('core:category'))
        self.assertQuerysetEqual(
            response.context['posts'],
            [category],
        )

    def test_two_past_category(self):
        """
        The categories index page may display multiple categories.
        """
        category1 = create_category(name="Past category 1.", days=-30)
        category2 = create_category(name="Past category 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['posts'],
            [category2, category1],
        )
