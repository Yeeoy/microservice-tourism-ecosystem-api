from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny
from information_center.views import HealthView
urlpatterns = [
    path('api/information-center/admin/', admin.site.urls),

    # API Schema and Documentation
    path('api/information-center/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/information-center/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/information-center/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/information-center/health/', HealthView.as_view()),
    # User-related APIs
    path('api/information-center/', include("information_center.urls")),
]