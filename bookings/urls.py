from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('', views.travel_list, name='travel_list'),
    path('book/<uuid:travel_id>/', views.book_travel, name='book_travel'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<uuid:booking_id>/', views.cancel_booking, name='cancel_booking'),
]