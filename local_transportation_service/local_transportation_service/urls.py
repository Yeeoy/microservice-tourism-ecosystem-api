from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny
from local_transportation.views import HealthView
urlpatterns = [
    path('api/local-transportation/admin/', admin.site.urls),

    # API Schema and Documentation
    path('api/local-transportation/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/local-transportation/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/local-transportation/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/local-transportation/health/', HealthView.as_view()),
    # User-related APIs
    path('api/local-transportation/', include("local_transportation.urls")),
]