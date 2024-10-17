from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CreateUserView,
    CustomTokenObtainPairView,  # 替换 CreateTokenView
    ManageUserView,
    EventLogViewSet,
    GenerateAndDownloadCSV,
    ClearEventLogView,
)

router = DefaultRouter()
router.register(r'event-logs', EventLogViewSet)

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # 更新这一行
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', ManageUserView.as_view(), name='me'),
    path('event-logs/download-csv/', GenerateAndDownloadCSV.as_view(), name='download-csv'),
    path('event-logs/clear/', ClearEventLogView.as_view(), name='clear-event-logs'),
    path('', include(router.urls)),
]