from django.shortcuts import render
from core.models.post import Post
from core.models.category import Category
from django.utils import timezone
from django.http import Http404

def post(request, slug):
    context = {
        'post': Post.objects.get(slug = slug)
    }
    
    return render(request, 'core/post.html', context)


def home(request):
    
    try:
        featuredPost = Post.objects.filter(
            status = 'PB',
            featured = True,
            created_at__lt = timezone.now(),
        ).order_by('-created_at')[0]
    except IndexError:
        featuredPost = None

    regularPosts = Post.objects.filter(
        status = 'PB',
        featured = False,
        created_at__lt = timezone.now()
    ).order_by('-created_at')

    context = {
        'featuredPost': featuredPost,
        'regularPosts': regularPosts
    }

    return render(request, 'core/home.html', context)
 

def category(request, slug):

    context = {
        'posts': Category.objects.get(slug = slug).posts.filter(
            status = 'PB',
            created_at__lt = timezone.now()
        ).order_by('-created_at'),
        'slug': slug
    }

    return render(request, 'core/category.html', context)