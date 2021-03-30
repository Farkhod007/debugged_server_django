from django.contrib.auth.models import User
from .base.time_fields_base import TimeFieldsBase 
from django.db import models

class Post(TimeFieldsBase):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    body = models.TextField() 
    image = models.ImageField(upload_to = 'posts') 
    excerpt = models.TextField()
    
    class Meta:
        db_table = "posts"

    def __str__(self):
        return self.title
