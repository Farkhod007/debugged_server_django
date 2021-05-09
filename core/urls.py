from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('category/<slug:slug>', views.category, name = 'category'),
    path('posts/<slug:slug>', views.post, name = 'post')
]