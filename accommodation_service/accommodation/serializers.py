from rest_framework import serializers
from .models import Accommodation, RoomType, RoomBooking, GuestService, FeedbackReview

class AccommodationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accommodation
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomBooking
        fields = ['id', 'room_type_id', 'accommodation_id', 'user_id', 'check_in_date', 'check_out_date', 'total_price', 'booking_status', 'payment_status']
        read_only_fields = ['user_id', 'total_price']

class AccommodationCalculatePriceSerializer(serializers.Serializer):
    accommodation_id = serializers.IntegerField()
    room_id = serializers.IntegerField()
    number_of_days = serializers.IntegerField(min_value=1)

class GuestServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestService
        fields = '__all__'

class FeedbackReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackReview
        fields = ['id', 'accommodation_id', 'user_id', 'rating', 'review', 'date']
        read_only_fields = ['user_id']