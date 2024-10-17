from django.apps import AppConfig
from .utils import register_service

class AccommodationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accommodation'
    
    def ready(self):
        pass
        # register_service()