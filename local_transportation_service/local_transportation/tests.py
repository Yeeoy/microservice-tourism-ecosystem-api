from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import TransportationProvider, RideBooking, RoutePlanning, TrafficUpdate
from django.contrib.auth import get_user_model
from datetime import date, timedelta, datetime
from decimal import Decimal

User = get_user_model()

@override_settings(
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': [],
        'DEFAULT_PERMISSION_CLASSES': [],
    },
    CONSUL_ENABLED=False,
    LOGGING_ENABLED=False
)
class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

class TransportationProviderViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.provider = TransportationProvider.objects.create(
            name="Test Provider",
            service_type="Taxi",
            base_fare=5.00,
            price_per_km=2.00,
            contact_info="test@provider.com"
        )

    def test_list_providers(self):
        url = reverse('local_transportation_services:transportationprovider-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_provider(self):
        url = reverse('local_transportation_services:transportationprovider-list')
        data = {
            "name": "New Provider",
            "service_type": "Bus",
            "base_fare": 3.00,
            "price_per_km": 1.50,
            "contact_info": "new@provider.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TransportationProvider.objects.count(), 2)

class RideBookingViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.provider = TransportationProvider.objects.create(
            name="Test Provider",
            service_type="Taxi",
            base_fare=5.00,
            price_per_km=2.00,
            contact_info="test@provider.com"
        )
        self.ride_booking = RideBooking.objects.create(
            user_id=self.user.id,
            provider_id=self.provider,
            pickup_location="Test Pickup",
            drop_off_location="Test Dropoff",
            ride_date=date.today() + timedelta(days=1),
            pickup_time="14:00:00",
            estimated_fare=20.00,
            booking_status=False
        )

    def test_list_ride_bookings(self):
        url = reverse('local_transportation_services:ridebooking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_ride_booking(self):
        url = reverse('local_transportation_services:ridebooking-list')
        data = {
            "user_id": self.user.id,
            "provider_id": self.provider.id,
            "pickup_location": "New Pickup",
            "drop_off_location": "New Dropoff",
            "ride_date": (date.today() + timedelta(days=2)).isoformat(),
            "pickup_time": "15:00:00",
            "estimated_fare": 25.00,
            "booking_status": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RideBooking.objects.count(), 2)

class RoutePlanningViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.provider = TransportationProvider.objects.create(
            name="Test Provider",
            service_type="Taxi",
            base_fare=5.00,
            price_per_km=2.00,
            contact_info="test@provider.com"
        )
        self.route_planning = RoutePlanning.objects.create(
            provider_id=self.provider,
            start_location="Test Start",
            end_location="Test End",
            distance=10.5,
            estimated_time="30 minutes"
        )

    def test_list_route_plannings(self):
        url = reverse('local_transportation_services:routeplanning-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_route_planning(self):
        url = reverse('local_transportation_services:routeplanning-list')
        data = {
            "provider_id": self.provider.id,
            "start_location": "New Start",
            "end_location": "New End",
            "distance": 15.0,
            "estimated_time": "45 minutes"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RoutePlanning.objects.count(), 2)

class TrafficUpdateViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.provider = TransportationProvider.objects.create(
            name="Test Provider",
            service_type="Taxi",
            base_fare=5.00,
            price_per_km=2.00,
            contact_info="test@provider.com"
        )
        self.traffic_update = TrafficUpdate.objects.create(
            provider_id=self.provider,
            update_time=datetime.now(),
            update_message="Test traffic update"
        )

    def test_list_traffic_updates(self):
        url = reverse('local_transportation_services:trafficupdate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_traffic_update(self):
        url = reverse('local_transportation_services:trafficupdate-list')
        data = {
            "provider_id": self.provider.id,
            "update_time": datetime.now().isoformat(),
            "update_message": "New traffic update"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TrafficUpdate.objects.count(), 2)

class TransportationProviderModelTest(TestCase):
    def test_provider_creation(self):
        provider = TransportationProvider.objects.create(
            name="Test Provider",
            service_type="Taxi",
            base_fare=5.00,
            price_per_km=2.00,
            contact_info="test@provider.com"
        )
        self.assertEqual(provider.name, "Test Provider")
        self.assertEqual(provider.base_fare, 5.00)

class RideBookingModelTest(TestCase):
    def setUp(self):
        self.provider = TransportationProvider.objects.create(
            name="Test Provider",
            service_type="Taxi",
            base_fare=5.00,
            price_per_km=2.00,
            contact_info="test@provider.com"
        )

    def test_ride_booking_creation(self):
        booking = RideBooking.objects.create(
            user_id=1,
            provider_id=self.provider,
            pickup_location="Test Pickup",
            drop_off_location="Test Dropoff",
            ride_date=date.today() + timedelta(days=1),
            pickup_time="14:00:00",
            estimated_fare=20.00,
            booking_status=False
        )
        self.assertEqual(booking.pickup_location, "Test Pickup")
        self.assertEqual(booking.estimated_fare, 20.00)

class RoutePlanningModelTest(TestCase):
    def setUp(self):
        self.provider = TransportationProvider.objects.create(
            name="Test Provider",
            service_type="Taxi",
            base_fare=5.00,
            price_per_km=2.00,
            contact_info="test@provider.com"
        )

    def test_route_planning_creation(self):
        route = RoutePlanning.objects.create(
            provider_id=self.provider,
            start_location="Test Start",
            end_location="Test End",
            distance=10.5,
            estimated_time="30 minutes"
        )
        self.assertEqual(route.start_location, "Test Start")
        self.assertEqual(route.distance, 10.5)

class TrafficUpdateModelTest(TestCase):
    def setUp(self):
        self.provider = TransportationProvider.objects.create(
            name="Test Provider",
            service_type="Taxi",
            base_fare=5.00,
            price_per_km=2.00,
            contact_info="test@provider.com"
        )

    def test_traffic_update_creation(self):
        update = TrafficUpdate.objects.create(
            provider_id=self.provider,
            update_time=datetime.now(),
            update_message="Test traffic update"
        )
        self.assertEqual(update.update_message, "Test traffic update")
