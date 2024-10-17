from rest_framework import serializers

from .models import Destination, Tour, EventNotification, TourBooking


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'
        read_only_fields = ['id']


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'
        read_only_fields = ['id']


class TourBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBooking
        fields = '__all__'
        read_only_fields = ['id']


class EventNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventNotification
        fields = '__all__'
        read_only_fields = ['id']
