from django.shortcuts import render
from django.templatetags.static import static
from core.models.category import Category
from core.models.post import Post

def home(request):
    featuredPost = Post.objects.filter(featured = True).order_by('created_at')[0]
    regularPosts = Post.objects.filter(featured = False)
    return render(request, 'core/home.html', {
        'featuredPost': featuredPost,
        'regularPosts': regularPosts
    })

def category(request, id):
    posts = Category.objects.get(pk = id).posts.all
    return render(request, 'core/categories.html', {
        'posts': posts
    })