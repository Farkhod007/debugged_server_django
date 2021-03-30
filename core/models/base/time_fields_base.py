from django.db import models

class TimeFieldsBase(models.Model):
    created_at = models.TimeField()
    updated_at = models.TimeField(default = None, blank = True)
    deleted_at = models.TimeField(default = None, blank = True, null = True)

    class Meta:
        abstract = True
        ordering = ['created_at']