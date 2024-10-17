from django.apps import AppConfig
from .utils import register_service

class EventOrganizersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'event_organizers'
    
    def ready(self):
        from .utils import register_service
        register_service()