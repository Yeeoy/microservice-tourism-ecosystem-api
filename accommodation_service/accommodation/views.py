from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from .models import Accommodation, RoomType, RoomBooking, GuestService, FeedbackReview
from .serializers import (
    AccommodationSerializer, RoomTypeSerializer, RoomBookingSerializer,
    AccommodationCalculatePriceSerializer, GuestServiceSerializer, FeedbackReviewSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from rest_framework import viewsets
from .auth_backend import JWTAuthBackend
from django.http import JsonResponse
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


@extend_schema(tags=["AM - Accommodation"])
class AccommodationViewSet(viewsets.ModelViewSet):
    queryset = Accommodation.objects.all()
    serializer_class = AccommodationSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Accommodation"

    def get_permissions(self):
        if settings.TESTING:
            return []
        return super().get_permissions()


@extend_schema(tags=["AM - Room Type"])
class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Room Type"

    def get_permissions(self):
        if settings.TESTING:
            return []
        return super().get_permissions()


@extend_schema(tags=["AM - Room Booking"])
class RoomBookingViewSet(viewsets.ModelViewSet):
    queryset = RoomBooking.objects.all()
    serializer_class = RoomBookingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    activity_name = "Room Booking"

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return RoomBooking.objects.all()
        return RoomBooking.objects.filter(user_id=user.id)

    @action(detail=False, methods=["post"], url_path="calculate-price", permission_classes=[AllowAny],
            serializer_class=AccommodationCalculatePriceSerializer)
    def calculate_price(self, request, *args, **kwargs):
        self.activity_name = "Calculate Room Price"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        accommodation_id = serializer.validated_data.get("accommodation_id")
        room_id = serializer.validated_data.get("room_id")
        number_of_days = serializer.validated_data.get("number_of_days")

        try:
            accommodation = Accommodation.objects.get(id=accommodation_id)
        except Accommodation.DoesNotExist:
            return Response({"detail": f"Accommodation with id {accommodation_id} does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            room = accommodation.types.get(id=room_id)
        except RoomType.DoesNotExist:
            return Response({"detail": f"Room with id {room_id} is not available for this accommodation."},
                            status=status.HTTP_404_NOT_FOUND)

        total_price = room.price_per_night * number_of_days

        return Response({
            "accommodation": accommodation.name,
            "room_type": room.room_type,
            "price_per_night": room.price_per_night,
            "number_of_days": number_of_days,
            "total_price": total_price,
        }, status=status.HTTP_200_OK)

    def get_permissions(self):
        if settings.TESTING:
            return []
        return super().get_permissions()


@extend_schema(tags=["AM - Guest Service"])
class GuestServiceViewSet(viewsets.ModelViewSet):
    queryset = GuestService.objects.all()
    serializer_class = GuestServiceSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Guest Service"

    @action(detail=False, methods=["get"], url_path="guestService/(?P<accommodation_id>[^/.]+)",
            permission_classes=[AllowAny])
    def get_guest_service_by_accommodation(self, request, accommodation_id=None):
        if not accommodation_id:
            return Response({"error": "The accommodation_id parameter is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        guest_services = self.get_guest_services_by_accommodation(accommodation_id)
        serializer = self.get_serializer(guest_services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_guest_services_by_accommodation(self, accommodation_id):
        return self.queryset.filter(accommodation_id=accommodation_id)

    def get_permissions(self):
        if settings.TESTING:
            return []
        return super().get_permissions()


@extend_schema(tags=["AM - Feedback Review"])
class FeedbackReviewViewSet(viewsets.ModelViewSet):
    queryset = FeedbackReview.objects.all()
    serializer_class = FeedbackReviewSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Feedback Review"

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return FeedbackReview.objects.all()
        return FeedbackReview.objects.filter(user_id=user.id)
    
    @action(
        detail=False,
        methods=["get"],
        url_path="accommodation/(?P<accommodation_id>[^/.]+)",
        permission_classes=[AllowAny],
    )
    def get_feedback_by_accommodation(self, request, accommodation_id=None):
        """
        Retrieve all feedback ratings for a given accommodation by accommodation_id
        """
        if not accommodation_id:
            return Response(
                {"error": "The accommodation_id parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        feedbacks = self.get_feedbacks_by_accommodation(accommodation_id)
        serializer = self.get_serializer(feedbacks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_feedbacks_by_accommodation(self, accommodation_id):
        """
        Helper method to get feedbacks by accommodation_id
        """
        return self.queryset.filter(accommodation_id=accommodation_id)

    def get_permissions(self):
        if settings.TESTING:
            return []
        return super().get_permissions()


@extend_schema(tags=["AM - Health"])
class HealthView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description='Check the health of the accommodation service',
        responses={200: {"description": "Service is healthy"}},
    )
    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
