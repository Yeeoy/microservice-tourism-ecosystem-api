from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny
from accommodation.views import HealthView

urlpatterns = [
    path('api/accommodation/admin/', admin.site.urls),

    # API Schema and Documentation
    path('api/accommodation/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/accommodation/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/accommodation/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/accommodation/health/', HealthView.as_view()),
    # User-related APIs
    path('api/accommodation/', include("accommodation.urls")),
]

