from django.db import models

# Create your models here.
class users(models.Model):
    pass
class posts(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(users,db_column='id',on_delete=models.CASCADE)
    name = models.CharField()
    desc = models.TextField()
    img = models.CharField()
    excerpt = models.CharField()
    created_at = models.TimeField()
    updated_at = models.TimeField()