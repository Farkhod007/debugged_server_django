from .base.time_fields_base import TimeFieldsBase 
from .base.category_tag_base import CategoryTagBase 
from django.db import models
from .post import Post


class Tag(CategoryTagBase, TimeFieldsBase):
    posts = models.ManyToManyField(Post)
    slug = models.SlugField(max_length = 250, null = True, blank = True)

    class Meta:
        db_table = "tags"