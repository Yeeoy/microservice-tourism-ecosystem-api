from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Event, VenueBooking, EventPromotion
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from decimal import Decimal

User = get_user_model()


@override_settings(
    REST_FRAMEWORK={
        "DEFAULT_AUTHENTICATION_CLASSES": [],
        "DEFAULT_PERMISSION_CLASSES": [],
    },
    CONSUL_ENABLED=False,
    LOGGING_ENABLED=False,
)
class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class EventViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event = Event.objects.create(
            name="Test Event",
            venue="Test Venue",
            description="Test Description",
            event_date=date.today() + timedelta(days=30),
            start_time="18:00:00",
            end_time="22:00:00",
            entry_fee=50.00,
            max_participants=100,
        )

    def test_list_events(self):
        url = reverse("event_organizers:event-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_event(self):
        url = reverse("event_organizers:event-list")
        data = {
            "name": "New Event",
            "venue": "New Venue",
            "description": "New Description",
            "event_date": (date.today() + timedelta(days=60)).isoformat(),
            "start_time": "19:00:00",
            "end_time": "23:00:00",
            "entry_fee": "75.00",
            "max_participants": 150,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)


class VenueBookingViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event = Event.objects.create(
            name="Test Event",
            venue="Test Venue",
            description="Test Description",
            event_date=date.today() + timedelta(days=30),
            start_time="18:00:00",
            end_time="22:00:00",
            entry_fee=50.00,
            max_participants=100,
        )

    def test_create_venue_booking(self):
        url = reverse("event_organizers:venue-booking-list")
        data = {
            "event_id": self.event.id,
            "booking_date": date.today().isoformat(),
            "number_of_tickets": 2,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VenueBooking.objects.count(), 1)

    def test_calculate_price(self):
        url = reverse("event_organizers:venue-booking-calculate-price")
        data = {"event": self.event.id, "number_of_tickets": 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data["total_amount"]), Decimal("100.00"))


class EventPromotionViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.event = Event.objects.create(
            name="Test Event",
            venue="Test Venue",
            description="Test Description",
            event_date=date.today() + timedelta(days=30),
            start_time="18:00:00",
            end_time="22:00:00",
            entry_fee=50.00,
            max_participants=100,
        )

    def test_create_event_promotion(self):
        url = reverse("event_organizers:event-promotion-list")
        data = {
            "event": self.event.id,
            "promotion_start_date": date.today().isoformat(),
            "promotion_end_date": (date.today() + timedelta(days=7)).isoformat(),
            "discount": "0.20",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EventPromotion.objects.count(), 1)


class EventModelTest(TestCase):
    def test_event_creation(self):
        event = Event.objects.create(
            name="Test Event",
            venue="Test Venue",
            description="Test Description",
            event_date=date.today() + timedelta(days=30),
            start_time="18:00:00",
            end_time="22:00:00",
            entry_fee=50.00,
            max_participants=100,
        )
        self.assertEqual(event.name, "Test Event")
        self.assertEqual(event.entry_fee, 50.00)


class VenueBookingModelTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Test Event",
            venue="Test Venue",
            description="Test Description",
            event_date=date.today() + timedelta(days=30),
            start_time="18:00:00",
            end_time="22:00:00",
            entry_fee=50.00,
            max_participants=100,
        )

    def test_venue_booking_creation(self):
        booking = VenueBooking.objects.create(
            event_id=self.event,
            user_id=1,
            booking_date=date.today(),
            number_of_tickets=2,
        )
        self.assertEqual(booking.number_of_tickets, 2)
        self.assertEqual(booking.total_amount, 100.00)


class EventPromotionModelTest(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            name="Test Event",
            venue="Test Venue",
            description="Test Description",
            event_date=date.today() + timedelta(days=30),
            start_time="18:00:00",
            end_time="22:00:00",
            entry_fee=50.00,
            max_participants=100,
        )

    def test_event_promotion_creation(self):
        promotion = EventPromotion.objects.create(
            event=self.event,
            promotion_start_date=date.today(),
            promotion_end_date=date.today() + timedelta(days=7),
            discount=0.20,
        )
        self.assertEqual(promotion.discount, 0.2)
