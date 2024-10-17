from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny
from customUser.views import HealthView
urlpatterns = [
    # ...其他 URL 配置...
    path('api/customUser/admin/', admin.site.urls),

    # API Schema and Documentation
    path('api/customUser/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/customUser/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/customUser/', SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/customUser/health/', HealthView.as_view()),
    # User-related APIs
    path('api/customUser/', include("customUser.urls")),
]