from django.shortcuts import render
from django.templatetags.static import static
from core.models.post import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'core/home.html', {'data': posts})
    