from django.apps import AppConfig


class TourismInformationCenterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'information_center'
    
    def ready(self):
        from .utils import register_service
        register_service()