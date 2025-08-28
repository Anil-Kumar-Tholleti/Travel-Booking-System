from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class TravelOption(models.Model):
    TYPE_CHOICES = [
        ('FLIGHT', 'Flight'),
        ('TRAIN', 'Train'),
        ('BUS', 'Bus'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    travel_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)  # Human-readable ID
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    total_seats = models.PositiveIntegerField(default=100)  # Track total capacity
    
    class Meta:
        ordering = ['date_time']
    
    def save(self, *args, **kwargs):
        if not self.travel_id:
            # Generate human-readable travel ID
            prefix = self.type[0]  # F, T, or B
            count = TravelOption.objects.filter(type=self.type).count() + 1
            self.travel_id = f"{prefix}{count:04d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.travel_id}: {self.type} {self.source} → {self.destination}"
    
    @property
    def is_available(self):
        return self.available_seats > 0 and self.date_time > timezone.now()


class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)  # Human-readable booking ID
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE)
    number_of_seats = models.PositiveIntegerField(default=1)  # Match requirement naming
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='CONFIRMED')
    
    class Meta:
        ordering = ['-booking_date']
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            # Generate human-readable booking ID
            from datetime import datetime
            date_str = datetime.now().strftime("%Y%m%d")
            count = Booking.objects.filter(booking_date__date=datetime.now().date()).count() + 1
            self.booking_id = f"BK{date_str}{count:03d}"
            
        # Ensure we have a booking date
        if not hasattr(self, 'booking_date') or not self.booking_date:
            self.booking_date = timezone.now()
        
        if not self.total_price:
            self.total_price = self.travel_option.price * self.number_of_seats
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username}"
    
    def cancel(self):
        if self.status == 'CONFIRMED' and self.travel_option.date_time > timezone.now():
            self.status = 'CANCELLED'
            self.travel_option.available_seats += self.number_of_seats
            self.travel_option.save()
            self.save()
            return True
        return False