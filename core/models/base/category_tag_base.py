from django.db import models

class CategoryTagBase(models.Model):
    parent_id = models.ForeignKey('self', on_delete = models.CASCADE)
    name = models.CharField(max_length = 255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
