from django.contrib import admin
from core.models.post import Post
from core.models.tag import Tag
from core.models.category import Category
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
    # prepopulated_fields = {"slug": ('title',)}
    inlines = [TagInline, CategoryInline]


class CategoryAdmin(admin.ModelAdmin):
    exclude = ['posts']


class TagAdmin(admin.ModelAdmin):
    exclude = ['posts']


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
