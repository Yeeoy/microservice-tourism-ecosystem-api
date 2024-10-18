from django.apps import AppConfig
from django.conf import settings

class RestaurantsCafesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant'

    def ready(self):
        if not settings.TESTING: 
            from .utils import register_service
            if settings.CONSUL_ENABLED:
                register_service()
            else:
                print("Consul service registration is disabled.")
