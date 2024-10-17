from django.contrib import admin
from .models import Accommodation, RoomType, RoomBooking, GuestService, FeedbackReview

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'star_rating', 'total_rooms')
    search_fields = ('name', 'location')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'price_per_night', 'max_occupancy', 'availability')

@admin.register(RoomBooking)
class RoomBookingAdmin(admin.ModelAdmin):
    list_display = ('accommodation_id', 'room_type_id', 'user_id', 'check_in_date', 'check_out_date', 'total_price', 'booking_status', 'payment_status')
    list_filter = ('booking_status', 'payment_status')

@admin.register(GuestService)
class GuestServiceAdmin(admin.ModelAdmin):
    list_display = ('accommodation_id', 'service_name', 'price', 'availability_hours')

@admin.register(FeedbackReview)
class FeedbackReviewAdmin(admin.ModelAdmin):
    list_display = ('accommodation_id', 'user_id', 'rating', 'date')  # 将 'user' 改为 'user_id'
    list_filter = ('rating',)