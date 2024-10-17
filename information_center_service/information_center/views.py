# Create your views here.
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .auth_backend import JWTAuthBackend
from .models import Destination, Tour, EventNotification, TourBooking
from .serializers import DestinationSerializer, TourSerializer, \
    EventNotificationSerializer, TourBookingSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.exceptions import NotFound
from django.core.exceptions import ValidationError


@extend_schema(tags=['TIC - Destination'])
class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Destination"  # 确保这里设置了正确的activity_name


@extend_schema(tags=['TIC - Tour'])
class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Tour"


@extend_schema(tags=['TIC - Event Notification'])
class EventNotificationViewSet(viewsets.ModelViewSet):
    queryset = EventNotification.objects.all()
    serializer_class = EventNotificationSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Event Notification"


@extend_schema(tags=['TIC - Tour Booking'])
class TourBookingViewSet(viewsets.ModelViewSet):
    queryset = TourBooking.objects.all()
    serializer_class = TourBookingSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Tour Booking"

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return TourBooking.objects.all()
        return TourBooking.objects.filter(user_id=user.id)

@extend_schema(tags=['TIC - Health'])
class HealthView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description='Check the health of the information center service',
        responses={200: {"description": "Service is healthy"}},
    )
    
    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
