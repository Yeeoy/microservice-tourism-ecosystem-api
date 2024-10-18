from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Restaurant, TableReservation, Menu, OnlineOrder
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

class RestaurantViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            location="Test Location",
            cuisine_type="Test Cuisine",
            opening_hours="9:00-22:00",
            contact_info="test@restaurant.com"
        )

    def test_list_restaurants(self):
        url = reverse('restaurants_cafes:restaurant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_restaurant(self):
        url = reverse('restaurants_cafes:restaurant-list')
        data = {
            "name": "New Restaurant",
            "location": "New Location",
            "cuisine_type": "New Cuisine",
            "opening_hours": "10:00-23:00",
            "contact_info": "new@restaurant.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 2)

class TableReservationViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            location="Test Location",
            cuisine_type="Test Cuisine",
            opening_hours="9:00-22:00",
            contact_info="test@restaurant.com"
        )
        self.reservation = TableReservation.objects.create(
            restaurant=self.restaurant,
            user_id=self.user.id,
            reservation_date=date.today() + timedelta(days=1),
            reservation_time="19:00:00",
            number_of_guests=2,
            reservation_status="Confirmed"
        )

    def test_list_reservations(self):
        url = reverse('restaurants_cafes:table-reservation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_reservation(self):
        url = reverse('restaurants_cafes:table-reservation-list')
        data = {
            "restaurant": self.restaurant.id,
            "user_id": self.user.id,  # 添加用户ID
            "reservation_date": (date.today() + timedelta(days=2)).isoformat(),
            "reservation_time": "20:00:00",
            "number_of_guests": 4,
            "reservation_status": "Pending"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TableReservation.objects.count(), 2)

class MenuViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            location="Test Location",
            cuisine_type="Test Cuisine",
            opening_hours="9:00-22:00",
            contact_info="test@restaurant.com"
        )
        self.menu_item = Menu.objects.create(
            restaurant=self.restaurant,
            item_name="Test Item",
            description="Test Description",
            price=10.99
        )

    def test_list_menu_items(self):
        url = reverse('restaurants_cafes:menu-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_menu_item(self):
        url = reverse('restaurants_cafes:menu-list')
        data = {
            "restaurant": self.restaurant.id,
            "item_name": "New Item",
            "description": "New Description",
            "price": 15.99
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)

    def test_get_menu_by_restaurant(self):
        url = reverse('restaurants_cafes:menu-get-menu-by-restaurant', kwargs={'restaurant_id': self.restaurant.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['item_name'], "Test Item")

class OnlineOrderViewSetTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            location="Test Location",
            cuisine_type="Test Cuisine",
            opening_hours="9:00-22:00",
            contact_info="test@restaurant.com"
        )
        self.menu_item = Menu.objects.create(
            restaurant=self.restaurant,
            item_name="Test Item",
            description="Test Description",
            price=10.99
        )

    def test_create_online_order(self):
        url = reverse('restaurants_cafes:online-order-list')
        data = {
            "restaurant": self.restaurant.id,
            "user_id": self.user.id,  # 添加用户ID
            "order_date": date.today().isoformat(),
            "order_time": datetime.now().time().isoformat(),
            "total_amount": "21.98",
            "order_status": "Pending",
            "order_items": [
                {
                    "menu_item_id": self.menu_item.id,
                    "quantity": 2
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OnlineOrder.objects.count(), 1)

    def test_calculate_price(self):
        url = reverse('restaurants_cafes:online-order-calculate-price')
        data = {
            "items": [
                {
                    "menu_item_id": self.menu_item.id,
                    "quantity": 2
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total_price']), Decimal('21.98'))

class RestaurantModelTest(TestCase):
    def test_restaurant_creation(self):
        restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            location="Test Location",
            cuisine_type="Test Cuisine",
            opening_hours="9:00-22:00",
            contact_info="test@restaurant.com"
        )
        self.assertEqual(restaurant.name, "Test Restaurant")
        self.assertEqual(restaurant.cuisine_type, "Test Cuisine")

class MenuModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            location="Test Location",
            cuisine_type="Test Cuisine",
            opening_hours="9:00-22:00",
            contact_info="test@restaurant.com"
        )

    def test_menu_item_creation(self):
        menu_item = Menu.objects.create(
            restaurant=self.restaurant,
            item_name="Test Item",
            description="Test Description",
            price=10.99
        )
        self.assertEqual(menu_item.item_name, "Test Item")
        self.assertEqual(menu_item.price, 10.99)

class OnlineOrderModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            location="Test Location",
            cuisine_type="Test Cuisine",
            opening_hours="9:00-22:00",
            contact_info="test@restaurant.com"
        )
        self.menu_item = Menu.objects.create(
            restaurant=self.restaurant,
            item_name="Test Item",
            description="Test Description",
            price=10.99
        )

    def test_online_order_creation(self):
        order = OnlineOrder.objects.create(
            user_id=1,
            restaurant=self.restaurant,
            order_date=date.today(),
            order_time=datetime.now().time(),
            total_amount=21.98,
            order_status="Pending"
        )
        self.assertEqual(order.total_amount, 21.98)
        self.assertEqual(order.order_status, "Pending")
