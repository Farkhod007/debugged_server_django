from django.db import models

class TimeFieldsBase(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True, blank = True)
    deleted_at = models.DateTimeField(default = None, blank = True, null = True)

    class Meta:
        abstract = True
        ordering = ['created_at']