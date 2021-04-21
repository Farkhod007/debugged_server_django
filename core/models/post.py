from django.contrib.auth.models import User
from .base.time_fields_base import TimeFieldsBase 
from django.db import models

class Post(TimeFieldsBase):
    published = 'PB'
    pending = 'PN'
    draft = 'DT'

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    body = models.TextField()
    image = models.ImageField(upload_to = 'posts') 
    excerpt = models.TextField()
    featured = models.BooleanField(default = False)
    STATUS_CHOICES = [
        (published, 'Published'),
        (pending, 'Pending'),
        (draft, 'Draft'),
    ]
    status = models.CharField(
        max_length = 2,
        choices = STATUS_CHOICES
    )

    class Meta:
        db_table = "posts"

    def __str__(self):
        return self.title

    # def get_year(self):
    #     return self.created_at.strftime('%Y')