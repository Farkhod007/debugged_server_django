from django.shortcuts import render
from django.templatetags.static import static
from .models import Post, Category

def home(request):
    feturedPost = Post.objects.get(featured = True)
    regularPosts = Post.objects.filter(featured = False)
    return render(request, 'core/home.html', {
        'feturedPost': feturedPost,
        'regularPosts': regularPosts
    })

def category(request, id):
    posts = Category.objects.get(pk = id).posts.all()
    return render(request, 'core/categories.html', {'posts': posts})