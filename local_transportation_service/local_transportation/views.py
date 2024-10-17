# Create your views here.
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .auth_backend import JWTAuthBackend
from .models import TransportationProvider, RideBooking, RoutePlanning, TrafficUpdate
from .serializers import TransportationServiceSerializer, RideBookingSerializer, \
    RoutePlanningSerializer, TrafficUpdateSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin


@extend_schema(tags=['LTS - Transportation Provider'])
class TransportationProviderViewSet(viewsets.ModelViewSet):
    queryset = TransportationProvider.objects.all()
    serializer_class = TransportationServiceSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Transportation Provider"


@extend_schema(tags=['LTS - Ride Booking'])
class RideBookingViewSet(viewsets.ModelViewSet):
    queryset = RideBooking.objects.all()
    serializer_class = RideBookingSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Ride Booking"


@extend_schema(tags=['LTS - Route Planning'])
class RoutePlanningViewSet(viewsets.ModelViewSet):
    queryset = RoutePlanning.objects.all()
    serializer_class = RoutePlanningSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Route Planning"


@extend_schema(tags=['LTS - Traffic Update'])
class TrafficUpdateViewSet(viewsets.ModelViewSet):
    queryset = TrafficUpdate.objects.all()
    serializer_class = TrafficUpdateSerializer
    authentication_classes = [JWTAuthBackend]
    permission_classes = [IsAuthenticatedOrReadOnly]
    activity_name = "Traffic Update"


@extend_schema(tags=['LTS - Health'])
class HealthView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        description='Check the health of the local transportation service',
        responses={200: {"description": "Service is healthy"}},
    )
    
    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)    