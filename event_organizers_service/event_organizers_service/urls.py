from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny
from event_organizers.views import HealthView
urlpatterns = [
    path('api/event-organizers/admin/', admin.site.urls),

    # API Schema and Documentation
    path('api/event-organizers/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/event-organizers/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/event-organizers/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/event-organizers/health/', HealthView.as_view()),
    # User-related APIs
    path('api/event-organizers/', include("event_organizers.urls")),
]