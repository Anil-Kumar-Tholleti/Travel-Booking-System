from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal
from .models import TravelOption, Booking


class BookingsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.travel_option = TravelOption.objects.create(
            type='FLIGHT',
            source='New York',
            destination='Los Angeles',
            date_time=timezone.now() + timezone.timedelta(days=7),
            price=Decimal('299.99'),
            available_seats=50,
            total_seats=100
        )

    def test_travel_option_creation(self):
        """Test TravelOption model creation and properties."""
        self.assertEqual(self.travel_option.type, 'FLIGHT')
        self.assertEqual(self.travel_option.source, 'New York')
        self.assertEqual(self.travel_option.destination, 'Los Angeles')
        self.assertTrue(self.travel_option.is_available)
        self.assertTrue(self.travel_option.can_book_seats(5))
        self.assertFalse(self.travel_option.can_book_seats(60))

    def test_booking_creation(self):
        """Test Booking model creation and total price calculation."""
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2
        )
        expected_total = self.travel_option.price * 2
        self.assertEqual(booking.total_price, expected_total)
        self.assertEqual(booking.status, 'CONFIRMED')
        self.assertTrue(booking.can_be_cancelled)

    def test_booking_process(self):
        """Test the complete booking process."""
        self.client.login(username='testuser', password='testpass123')
        
        # Test booking form
        response = self.client.post(
            reverse('bookings:book_travel', args=[self.travel_option.travel_id]),
            {'number_of_seats': 3}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful booking
        
        # Check if booking was created
        booking = Booking.objects.filter(user=self.user).first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.number_of_seats, 3)
        self.assertEqual(booking.travel_option, self.travel_option)
        
        # Check if seats were deducted
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, 47)

    def test_booking_validation(self):
        """Test booking validation for insufficient seats."""
        self.client.login(username='testuser', password='testpass123')
        
        # Try to book more seats than available
        response = self.client.post(
            reverse('bookings:book_travel', args=[self.travel_option.travel_id]),
            {'number_of_seats': 60}
        )
        
        # Should not create booking
        self.assertFalse(Booking.objects.filter(user=self.user).exists())

    def test_booking_cancellation(self):
        """Test booking cancellation and seat restoration."""
        # Create a booking
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=5
        )
        
        # Update available seats to reflect the booking
        self.travel_option.available_seats -= 5
        self.travel_option.save()
        
        initial_seats = self.travel_option.available_seats
        
        # Cancel the booking
        result = booking.cancel_booking()
        self.assertTrue(result)
        
        # Check booking status
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'CANCELLED')
        
        # Check if seats were restored
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, initial_seats + 5)

    def test_travel_list_view(self):
        """Test travel list view and filtering."""
        response = self.client.get(reverse('bookings:travel_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New York')
        self.assertContains(response, 'Los Angeles')
        
        # Test filtering
        response = self.client.get(reverse('bookings:travel_list'), {
            'type': 'FLIGHT',
            'source': 'New York'
        })
        self.assertEqual(response.status_code, 200)

    def test_my_bookings_view(self):
        """Test my bookings view."""
        self.client.login(username='testuser', password='testpass123')
        
        # Create a booking
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2
        )
        
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(booking.booking_id))

    def test_unauthorized_booking_access(self):
        """Test that unauthorized users cannot access booking views."""
        # Try to access booking without login
        response = self.client.get(
            reverse('bookings:book_travel', args=[self.travel_option.travel_id])
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Try to access my bookings without login
        response = self.client.get(reverse('bookings:my_bookings'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_seat_availability_validation(self):
        """Test seat availability validation in concurrent scenarios."""
        # Simulate concurrent booking attempts
        self.client.login(username='testuser', password='testpass123')
        
        # Create another user
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Reduce available seats to test edge case
        self.travel_option.available_seats = 2
        self.travel_option.save()
        
        # First booking should succeed
        response1 = self.client.post(
            reverse('bookings:book_travel', args=[self.travel_option.travel_id]),
            {'number_of_seats': 1}
        )
        self.assertEqual(response1.status_code, 302)
        
        # Second booking for remaining seat should succeed
        client2 = Client()
        client2.login(username='testuser2', password='testpass123')
        response2 = client2.post(
            reverse('bookings:book_travel', args=[self.travel_option.travel_id]),
            {'number_of_seats': 1}
        )
        self.assertEqual(response2.status_code, 302)
        
        # Check final seat count
        self.travel_option.refresh_from_db()
        self.assertEqual(self.travel_option.available_seats, 0)
