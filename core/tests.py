import datetime
from unittest import result

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from core.models.category import Category
from core.models.post import Post
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.db.models import Max


def create_post(user, title, featured, days, status = 'PB'):
    post = Post.objects.create(
        user = user, 
        title = title,
        slug = slugify(title),
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


def create_category(name, days):
        
    return Category.objects.create(
        name = name, 
        slug = slugify(name),
        created_at = timezone.now() + datetime.timedelta(days = days)
    )


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


    def test_regular_post_must_be_ordered_in_descending_by_created_at(self):
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


class CategoryViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username = 'Tester', 
            email = 'tester@admin.com', 
            password = 'password'
        )


    def test_category_must_exist(self):
        """
        Category must exist
        """
        category = create_category(
            name = "Example category", 
            days = -3
        )
        post = create_post(
            user = self.user,
            title = "Post", 
            featured = False, 
            days = -3
        )
        category.posts.add(post)

        response = self.client.get(reverse(
            'core:category', 
            kwargs = {'slug': slugify("Example category")})
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], [repr(post)])
    

    def test_posts_of_category_must_be_ordered_in_descending_by_created_at(self):
        """
        Posts of category must be ordered in descending by created_at field
        """
        firstCategory = create_category(
            name = "First category", 
            days = -1
        )

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
        firstCategory.posts.add(firstPost, secondPost)

        response = self.client.get(reverse(
            'core:category', 
            kwargs = {'slug': slugify("First category")})
        )

        self.assertQuerysetEqual(
            response.context['posts'],
            [repr(secondPost), repr(firstPost)]
        )
        

    def test_category_must_not_be_displayed_in_own_post_caption(self):
        """
        Category must not be displayed in own post's caption
        """
        category = create_category(
            name = "Front End", 
            days = -1
        )
        post = create_post(
            user = self.user, 
            title = "First post",
            featured = False, 
            days = -3
        )
        category.posts.add(post)

        link = reverse('core:category', kwargs = {'slug': slugify("Front End")})

        response = self.client.get(link)

        self.assertNotContains(
            response, 
            link
        )


    def test_each_post_of_category_status_must_be_equal_to_published(self):
        """
        Each posts of category status must be euqal to published
        """
        category = create_category(
            name = "Front End", 
            days = -1
        )
        firstPost = create_post(
            user = self.user, 
            title = "First post",
            featured = False, 
            days = -1
        )
        secondPost = create_post(
            user = self.user, 
            title = "Second post",
            featured = False, 
            days = -2,
            status = 'DT'
        )
        category.posts.add(firstPost, secondPost)

        response = self.client.get(reverse('core:category', kwargs = {
            'slug': slugify("Front End")
        }))
        
        self.assertQuerysetEqual(
            response.context['posts'], 
            [repr(firstPost)]
        )    
                

    def test_each_post_of_category_must_be_published_in_the_past(self):
        """
        Each posts of category must be published in the past
        """
        category = create_category(
            name = "Front End", 
            days = -1
        )
        pastPost = create_post(
            user = self.user, 
            title = "Past post",
            featured = False, 
            days = -1
        )
        futurePost = create_post(
            user = self.user, 
            title = "Future post",
            featured = False, 
            days = 2
        )
        category.posts.add(pastPost, futurePost)
                 
        response = self.client.get(reverse('core:category', kwargs = {
            'slug': slugify("Front End")
        }))

        self.assertQuerysetEqual(
            response.context['posts'],
            [repr(pastPost)]
        )