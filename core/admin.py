from django.contrib import admin
from .models import Post, Tag, Category
from django import forms
from tinymce.widgets import TinyMCE


class TagInline(admin.TabularInline):
    model = Tag.posts.through
    extra = 1

class CategoryInline(admin.TabularInline):
    model = Category.posts.through
    extra = 1

class PostForm(forms.ModelForm):
    body = forms.CharField(widget = TinyMCE())

    class Meta:
        model = Post
        exclude = []


class PostAdmin(admin.ModelAdmin):
    form = PostForm
    inlines = [TagInline, CategoryInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)
