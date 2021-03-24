from django.contrib.auth.models import User
from django.db import models
     
class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    body = models.TextField() 
    image = models.ImageField(upload_to = 'posts') 
    excerpt = models.TextField()
    created_at = models.TimeField()
    updated_at = models.TimeField()
    deleted_at = models.TimeField(default = None, blank = True, null = True)

    def __str__(self):
        return self.title
    