from django.apps import AppConfig


class RestaurantsCafesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant'

    def ready(self):
        from .utils import register_service
        register_service()
