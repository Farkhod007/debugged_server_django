from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from core.models.post import Post
        from core.models.tag import Tag
        from core.models.category import Category