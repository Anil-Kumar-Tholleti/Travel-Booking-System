from django.contrib import admin
from .models import TravelOption, Booking


@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ['type', 'source', 'destination', 'date_time', 'price', 'available_seats']
    list_filter = ['type', 'source', 'destination']
    search_fields = ['source', 'destination']
    ordering = ['date_time']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'travel_option', 'number_of_seats', 'total_price', 'status', 'booking_date']
    list_filter = ['status', 'travel_option__type']
    search_fields = ['user__username', 'travel_option__source', 'travel_option__destination']
    readonly_fields = ['total_price', 'booking_date']