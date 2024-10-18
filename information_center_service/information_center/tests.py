from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Destination, Tour, TourBooking, EventNotification
from django.contrib.auth import get_user_model
from datetime import date, timedelta
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

class DestinationViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.destination = Destination.objects.create(
            name="Test Destination",
            category="Test Category",
            description="Test Description",
            location="Test Location",
            opening_hours="9:00-17:00",
            contact_info="test@destination.com"
        )

    def test_list_destinations(self):
        url = reverse('information_center:destination-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_destination(self):
        url = reverse('information_center:destination-list')
        data = {
            "name": "New Destination",
            "category": "New Category",
            "description": "New Description",
            "location": "New Location",
            "opening_hours": "10:00-18:00",
            "contact_info": "new@destination.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Destination.objects.count(), 2)

class TourViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.destination = Destination.objects.create(
            name="Test Destination",
            category="Test Category",
            description="Test Description",
            location="Test Location",
            opening_hours="9:00-17:00",
            contact_info="test@destination.com"
        )
        self.tour = Tour.objects.create(
            destination=self.destination,
            name="Test Tour",
            tour_type="Test Type",
            duration="2 hours",
            price_per_person=50.00,
            max_capacity=20,
            tour_date=date.today() + timedelta(days=30),
            guide_name="Test Guide"
        )

    def test_list_tours(self):
        url = reverse('information_center:tour-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_tour(self):
        url = reverse('information_center:tour-list')
        data = {
            "destination": self.destination.id,
            "name": "New Tour",
            "tour_type": "New Type",
            "duration": "3 hours",
            "price_per_person": 75.00,
            "max_capacity": 30,
            "tour_date": (date.today() + timedelta(days=60)).isoformat(),
            "guide_name": "New Guide"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tour.objects.count(), 2)

class TourBookingViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.destination = Destination.objects.create(
            name="Test Destination",
            category="Test Category",
            description="Test Description",
            location="Test Location",
            opening_hours="9:00-17:00",
            contact_info="test@destination.com"
        )
        self.tour = Tour.objects.create(
            destination=self.destination,
            name="Test Tour",
            tour_type="Test Type",
            duration="2 hours",
            price_per_person=50.00,
            max_capacity=20,
            tour_date=date.today() + timedelta(days=30),
            guide_name="Test Guide"
        )

    def test_create_tour_booking(self):
        url = reverse('information_center:tour-booking-list')
        data = {
            "tour_id": self.tour.id,
            "user_id": self.user.id,  # 添加用户ID
            "total_price": 100.00,
            "booking_status": False,
            "payment_status": False
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TourBooking.objects.count(), 1)

class EventNotificationViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event_notification = EventNotification.objects.create(
            title="Test Event",
            description="Test Description",
            event_date=date.today() + timedelta(days=30),
            location="Test Location",
            entry_fee=25.00,
            target_audience="Test Audience"
        )

    def test_list_event_notifications(self):
        url = reverse('information_center:event-notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_event_notification(self):
        url = reverse('information_center:event-notification-list')
        data = {
            "title": "New Event",
            "description": "New Description",
            "event_date": (date.today() + timedelta(days=60)).isoformat(),
            "location": "New Location",
            "entry_fee": 30.00,
            "target_audience": "New Audience"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventNotification.objects.count(), 2)

class DestinationModelTest(TestCase):
    def test_destination_creation(self):
        destination = Destination.objects.create(
            name="Test Destination",
            category="Test Category",
            description="Test Description",
            location="Test Location",
            opening_hours="9:00-17:00",
            contact_info="test@destination.com"
        )
        self.assertEqual(destination.name, "Test Destination")
        self.assertEqual(destination.category, "Test Category")

class TourModelTest(TestCase):
    def setUp(self):
        self.destination = Destination.objects.create(
            name="Test Destination",
            category="Test Category",
            description="Test Description",
            location="Test Location",
            opening_hours="9:00-17:00",
            contact_info="test@destination.com"
        )

    def test_tour_creation(self):
        tour = Tour.objects.create(
            destination=self.destination,
            name="Test Tour",
            tour_type="Test Type",
            duration="2 hours",
            price_per_person=50.00,
            max_capacity=20,
            tour_date=date.today() + timedelta(days=30),
            guide_name="Test Guide"
        )
        self.assertEqual(tour.name, "Test Tour")
        self.assertEqual(tour.price_per_person, 50.00)

class TourBookingModelTest(TestCase):
    def setUp(self):
        self.destination = Destination.objects.create(
            name="Test Destination",
            category="Test Category",
            description="Test Description",
            location="Test Location",
            opening_hours="9:00-17:00",
            contact_info="test@destination.com"
        )
        self.tour = Tour.objects.create(
            destination=self.destination,
            name="Test Tour",
            tour_type="Test Type",
            duration="2 hours",
            price_per_person=50.00,
            max_capacity=20,
            tour_date=date.today() + timedelta(days=30),
            guide_name="Test Guide"
        )

    def test_tour_booking_creation(self):
        booking = TourBooking.objects.create(
            tour_id=self.tour,
            user_id=1,
            total_price=100.00
        )
        self.assertEqual(booking.total_price, 100.00)

class EventNotificationModelTest(TestCase):
    def test_event_notification_creation(self):
        event_notification = EventNotification.objects.create(
            title="Test Event",
            description="Test Description",
            event_date=date.today() + timedelta(days=30),
            location="Test Location",
            entry_fee=25.00,
            target_audience="Test Audience"
        )
        self.assertEqual(event_notification.title, "Test Event")
        self.assertEqual(event_notification.entry_fee, 25.00)
