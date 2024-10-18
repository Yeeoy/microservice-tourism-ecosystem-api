from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Accommodation, RoomType, RoomBooking, GuestService, FeedbackReview
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()

# 全局禁用认证和权限
@override_settings(
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': [],
        'DEFAULT_PERMISSION_CLASSES': [],
    },
    CONSUL_ENABLED=False,  # 禁用Consul服务注册
    LOGGING_ENABLED=False  # 禁用日志记录
)
class BaseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

class AccommodationViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            location="Test City",
            star_rating=4,
            total_rooms=100,
            amenities="WiFi, Pool",
            check_in_time="14:00",
            check_out_time="11:00",
            contact_info="test@hotel.com"
        )

    def test_list_accommodations(self):
        url = reverse('accommodation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_accommodation(self):
        self.room = RoomType.objects.create(
            room_type='Test type',
            price_per_night=100.00,
            max_occupancy=20,
            availability=True
        )

        url = reverse('accommodation-list')
        data = {
            "name": "New Hotel",
            "location": "New City",
            "star_rating": 5,
            "total_rooms": 200,
            "amenities": "WiFi, Pool, Gym",
            "check_in_time": "15:00:00",
            "check_out_time": "12:00:00",
            "contact_info": "new@hotel.com",
            "types": [self.room.id]
        }
        response = self.client.post(url, data, format='json')
        
        if response.status_code != status.HTTP_201_CREATED:
            print("Accommodation count:", Accommodation.objects.count())
            print("All accommodations:", list(Accommodation.objects.all().values()))
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Accommodation.objects.count(), 2)

class RoomBookingViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            location="Test City",
            star_rating=4,
            total_rooms=100,
            amenities="WiFi, Pool",
            check_in_time="14:00",
            check_out_time="11:00",
            contact_info="test@hotel.com"
        )
        self.room_type = RoomType.objects.create(
            room_type="Standard",
            price_per_night=100.00,
            max_occupancy=2
        )
        self.accommodation.types.add(self.room_type)

    def test_create_room_booking(self):
        url = reverse('roombooking-list')
        data = {
            "room_type_id": self.room_type.id,
            "accommodation_id": self.accommodation.id,
            "check_in_date": date.today().isoformat(),
            "check_out_date": (date.today() + timedelta(days=2)).isoformat(),
            "user_id": self.user.id  # 添加用��ID
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RoomBooking.objects.count(), 1)

    def test_calculate_price(self):
        url = reverse('roombooking-calculate-price')
        data = {
            "accommodation_id": self.accommodation.id,
            "room_id": self.room_type.id,
            "number_of_days": 3
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_price'], 300.00)

class GuestServiceViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            location="Test City",
            star_rating=4,
            total_rooms=100,
            amenities="WiFi, Pool",
            check_in_time="14:00",
            check_out_time="11:00",
            contact_info="test@hotel.com"
        )
        self.guest_service = GuestService.objects.create(
            accommodation_id=self.accommodation,
            service_name="Room Service",
            price=50.00,
            availability_hours="24/7"
        )

    def test_list_guest_services(self):
        url = reverse('guestservice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_guest_service_by_accommodation(self):
        url = reverse('guestservice-get-guest-service-by-accommodation', kwargs={'accommodation_id': self.accommodation.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['service_name'], "Room Service")

class FeedbackReviewViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            location="Test City",
            star_rating=4,
            total_rooms=100,
            amenities="WiFi, Pool",
            check_in_time="14:00",
            check_out_time="11:00",
            contact_info="test@hotel.com"
        )

    def test_create_feedback(self):
        url = reverse('feedbackreview-list')
        data = {
            "accommodation_id": self.accommodation.id,
            "rating": 5,
            "review": "Great hotel!",
            "date": date.today().isoformat(),
            "user_id": self.user.id  # 添加用户ID
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FeedbackReview.objects.count(), 1)

    def test_get_feedback_by_accommodation(self):
        FeedbackReview.objects.create(
            accommodation_id=self.accommodation,
            user_id=self.user.id,
            rating=5,
            review="Great hotel!",
            date=date.today()
        )
        url = reverse('feedbackreview-get-feedback-by-accommodation', kwargs={'accommodation_id': self.accommodation.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['rating'], 5)

# 保留原有的模型测试
class AccommodationModelTest(TestCase):
    def setUp(self):
        self.accommodation = Accommodation.objects.create(
            name="Test Hotel",
            location="Test City",
            star_rating=4,
            total_rooms=100,
            amenities="WiFi, Pool",
            check_in_time="14:00",
            check_out_time="11:00",
            contact_info="test@hotel.com"
        )

    def test_accommodation_creation(self):
        self.assertEqual(self.accommodation.name, "Test Hotel")
        self.assertEqual(self.accommodation.star_rating, 4)

class RoomTypeModelTest(TestCase):
    def setUp(self):
        self.room_type = RoomType.objects.create(
            room_type="Standard",
            price_per_night=100.00,
            max_occupancy=2
        )

    def test_room_type_creation(self):
        self.assertEqual(self.room_type.room_type, "Standard")
        self.assertEqual(self.room_type.price_per_night, 100.00)
