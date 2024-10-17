from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccommodationViewSet, RoomTypeViewSet, RoomBookingViewSet, GuestServiceViewSet, FeedbackReviewViewSet

router = DefaultRouter()
router.register(r'accommodations', AccommodationViewSet)
router.register(r'room-types', RoomTypeViewSet)
router.register(r'room-bookings', RoomBookingViewSet)
router.register(r'guest-services', GuestServiceViewSet)
router.register(r'feedback-reviews', FeedbackReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]