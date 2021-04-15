from django.contrib import admin
from .models import Post
# from django import forms
# from tinymce.widgets import TinyMCE


# class PostForm(forms.ModelForm):
#     body = forms.CharField(widget = TinyMCE(attrs = {'cols': 80, 'rows': 10}))

#     class Meta:
#         model = Post


# class PostAdmin(admin.ModelAdmin):
#     form = PostForm


admin.site.register(Post)
