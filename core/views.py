from django.shortcuts import render
from django.templatetags.static import static
from core.models.post import Post
from core.models.category import Category
from django.utils import timezone


def home(request):

    try:
        featuredPost = Post.objects.filter(
            featured = True,
            created_at__lt = timezone.now()
        ).order_by('-created_at')[0]
    except IndexError:
        featuredPost = None

    regularPosts = Post.objects.filter(
        featured = False,
        created_at__lt = timezone.now()
    ).order_by('-created_at')

    context = {
        'featuredPost': featuredPost,
        'regularPosts': regularPosts
    }

    return render(request, 'core/home.html', context)


def category(request, id):

    context = {
        'posts': Category.objects.get(pk = id).posts.all
    }

    return render(request, 'core/categories.html', context)