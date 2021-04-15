from django.shortcuts import render
from django.templatetags.static import static
from core.models.post import Post

def home(request):
    feturedPost = Post.objects.get(featured = True)
    regularPosts = Post.objects.filter(featured = False)
    return render(request, 'core/home.html', {
        'feturedPost': feturedPost,
        'regularPosts': regularPosts
    })
    