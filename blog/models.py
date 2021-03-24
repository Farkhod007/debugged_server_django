from django.db import models

# Create your models here.
class User(models.Model):
    pass

    def __str__(self):
        return self.name
     

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 255)
    desc = models.TextField() 
    img = models.CharField(max_length = 255)
    excerpt = models.TextField()
    created_at = models.TimeField()
    updated_at = models.TimeField()

    def __str__(self):
        return self.name
    