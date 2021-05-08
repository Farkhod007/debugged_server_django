from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home, name = 'home'),
    path('category/<int:id>', views.category, name = 'category'),
    path('posts/<int:id>', views.post, name = 'post')
]