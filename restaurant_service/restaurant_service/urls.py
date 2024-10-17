from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny
from restaurant.views import HealthView
urlpatterns = [
    path('api/restaurant/admin/', admin.site.urls),

    # API Schema and Documentation
    path('api/restaurant/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/restaurant/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/restaurant/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/restaurant/health/', HealthView.as_view()),
    # User-related APIs
    path('api/restaurant/', include("restaurant.urls")),
]