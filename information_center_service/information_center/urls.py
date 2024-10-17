from rest_framework.routers import DefaultRouter

from .views import DestinationViewSet, TourViewSet, EventNotificationViewSet, \
    TourBookingViewSet

app_name = 'information_center'

router = DefaultRouter()
router.register('destinations', DestinationViewSet, basename='destination')
router.register('tours', TourViewSet, basename='tour')
router.register('event-notifications', EventNotificationViewSet, basename='event-notification')
router.register('tour-bookings', TourBookingViewSet, basename='tour-booking')

urlpatterns = router.urls
