from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from bookings.models import TravelOption


class Command(BaseCommand):
    help = 'Load sample travel data for development and testing'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample travel data...')
        
        # Clear existing data
        TravelOption.objects.all().delete()
        
        sample_data = [
            # Flights
            {
                'type': 'FLIGHT',
                'source': 'New York',
                'destination': 'Los Angeles',
                'date_time': timezone.now() + timedelta(days=7, hours=8),
                'price': Decimal('299.99'),
                'available_seats': 50,
                'total_seats': 100
            },
            {
                'type': 'FLIGHT',
                'source': 'Chicago',
                'destination': 'Miami',
                'date_time': timezone.now() + timedelta(days=5, hours=14),
                'price': Decimal('189.99'),
                'available_seats': 75,
                'total_seats': 150
            },
            {
                'type': 'FLIGHT',
                'source': 'San Francisco',
                'destination': 'Seattle',
                'date_time': timezone.now() + timedelta(days=10, hours=10),
                'price': Decimal('149.99'),
                'available_seats': 30,
                'total_seats': 80
            },
            {
                'type': 'FLIGHT',
                'source': 'Boston',
                'destination': 'Denver',
                'date_time': timezone.now() + timedelta(days=12, hours=16),
                'price': Decimal('249.99'),
                'available_seats': 45,
                'total_seats': 120
            },
            
            # Trains
            {
                'type': 'TRAIN',
                'source': 'Chicago',
                'destination': 'Denver',
                'date_time': timezone.now() + timedelta(days=5, hours=9),
                'price': Decimal('89.99'),
                'available_seats': 80,
                'total_seats': 120
            },
            {
                'type': 'TRAIN',
                'source': 'New York',
                'destination': 'Washington DC',
                'date_time': timezone.now() + timedelta(days=3, hours=7),
                'price': Decimal('65.99'),
                'available_seats': 100,
                'total_seats': 200
            },
            {
                'type': 'TRAIN',
                'source': 'Los Angeles',
                'destination': 'San Diego',
                'date_time': timezone.now() + timedelta(days=8, hours=11),
                'price': Decimal('39.99'),
                'available_seats': 150,
                'total_seats': 180
            },
            {
                'type': 'TRAIN',
                'source': 'Portland',
                'destination': 'Seattle',
                'date_time': timezone.now() + timedelta(days=6, hours=13),
                'price': Decimal('45.99'),
                'available_seats': 90,
                'total_seats': 140
            },
            
            # Buses
            {
                'type': 'BUS',
                'source': 'Miami',
                'destination': 'Orlando',
                'date_time': timezone.now() + timedelta(days=3, hours=8),
                'price': Decimal('25.99'),
                'available_seats': 35,
                'total_seats': 40
            },
            {
                'type': 'BUS',
                'source': 'Atlanta',
                'destination': 'Nashville',
                'date_time': timezone.now() + timedelta(days=4, hours=12),
                'price': Decimal('32.99'),
                'available_seats': 28,
                'total_seats': 45
            },
            {
                'type': 'BUS',
                'source': 'Phoenix',
                'destination': 'Las Vegas',
                'date_time': timezone.now() + timedelta(days=9, hours=15),
                'price': Decimal('42.99'),
                'available_seats': 20,
                'total_seats': 50
            },
            {
                'type': 'BUS',
                'source': 'Dallas',
                'destination': 'Austin',
                'date_time': timezone.now() + timedelta(days=7, hours=10),
                'price': Decimal('29.99'),
                'available_seats': 38,
                'total_seats': 55
            },
            
            # Additional options for variety
            {
                'type': 'FLIGHT',
                'source': 'Las Vegas',
                'destination': 'New York',
                'date_time': timezone.now() + timedelta(days=14, hours=6),
                'price': Decimal('319.99'),
                'available_seats': 25,
                'total_seats': 90
            },
            {
                'type': 'TRAIN',
                'source': 'San Francisco',
                'destination': 'Los Angeles',
                'date_time': timezone.now() + timedelta(days=11, hours=8),
                'price': Decimal('79.99'),
                'available_seats': 110,
                'total_seats': 160
            },
            {
                'type': 'BUS',
                'source': 'Houston',
                'destination': 'New Orleans',
                'date_time': timezone.now() + timedelta(days=13, hours=14),
                'price': Decimal('38.99'),
                'available_seats': 42,
                'total_seats': 48
            }
        ]
        
        created_count = 0
        for data in sample_data:
            travel_option = TravelOption.objects.create(**data)
            created_count += 1
            self.stdout.write(f'Created: {travel_option}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully loaded {created_count} travel options')
        )
