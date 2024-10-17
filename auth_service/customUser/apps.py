from django.apps import AppConfig


class CustomuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customUser'

    def ready(self):
        from .utils import register_service
        register_service()