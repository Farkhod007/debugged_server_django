from django.contrib import admin
from .models import Post, Tag, Category
from django import forms
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    body = forms.CharField(widget = TinyMCE())

    class Meta:
        model = Post
        exclude = []


class PostAdmin(admin.ModelAdmin):
    form = PostForm


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)
