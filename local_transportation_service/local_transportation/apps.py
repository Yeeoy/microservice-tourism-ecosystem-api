from django.apps import AppConfig


class LocalTransportationServicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'local_transportation'

    def ready(self):
        from .utils import register_service
        register_service()