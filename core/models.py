from django.contrib.auth.models import User
from django.db import models
     
class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 255)
    body = models.TextField() 
    image = models.ImageField(upload_to = 'posts') 
    excerpt = models.TextField()
    created_at = models.TimeField()
    updated_at = models.TimeField(default = None, blank = True)
    deleted_at = models.TimeField(default = None, blank = True, null = True)
    
    class Meta:
        db_table = "posts"

    def __str__(self):
        return self.title
class categories(models.Model):
    # parent_id = models.ForeignKey(categories,on_delete = models.CASCADE) #shu qatorda error bervotti
    name = models.CharField(max_length = 255)
    created_at = models.TimeField()
    updated_at = models.TimeField(default = None, blank = True)
class tags(models.Model):
    # parent_id = models.ForeignKey(tags,on_delete = models.CASCADE) #shu qatorda error bervotti
    name = models.CharField(max_length = 255)
    created_at = models.TimeField()
    updated_at = models.TimeField(default = None,blank = True)
    