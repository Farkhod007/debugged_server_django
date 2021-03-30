from django.shortcuts import render
from django.templatetags.static import static

def home(request):
    posts = {
        'title': 'Lorem Ipsum', 
        'image': static('images/nature.jpeg'), 
        'desc': 'The default configuration is purposefully kept to a minimum.The Jinja2 backend adds the globals request, csrf_input, and csrf_token to the context.'
    }
    return render(request, 'core/home.html', {'posts': posts})
    