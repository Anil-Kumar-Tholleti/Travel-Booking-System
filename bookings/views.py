from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import transaction
from django.utils import timezone
from .models import TravelOption, Booking
from .forms import BookingForm, FilterForm


def travel_list(request):
    travels = TravelOption.objects.filter(
        date_time__gt=timezone.now(),
        available_seats__gt=0
    )
    
    form = FilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['type']:
            travels = travels.filter(type=form.cleaned_data['type'])
        if form.cleaned_data['source']:
            travels = travels.filter(source__icontains=form.cleaned_data['source'])
        if form.cleaned_data['destination']:
            travels = travels.filter(destination__icontains=form.cleaned_data['destination'])
        if form.cleaned_data['date']:
            travels = travels.filter(date_time__date=form.cleaned_data['date'])
    
    paginator = Paginator(travels, 6)
    page = paginator.get_page(request.GET.get('page'))
    
    return render(request, 'bookings/travel_list.html', {
        'page_obj': page,
        'form': form
    })


@login_required
def book_travel(request, travel_id):
    travel = get_object_or_404(TravelOption, id=travel_id)
    
    if not travel.is_available:
        messages.error(request, 'This travel option is not available.')
        return redirect('bookings:travel_list')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, travel_option=travel)
        if form.is_valid():
            with transaction.atomic():
                travel = TravelOption.objects.select_for_update().get(id=travel_id)
                seats = form.cleaned_data['number_of_seats']
                
                if travel.available_seats >= seats:
                    booking = form.save(commit=False)
                    booking.user = request.user
                    booking.travel_option = travel
                    booking.total_price = travel.price * seats
                    booking.save()
                    
                    travel.available_seats -= seats
                    travel.save()
                    
                    messages.success(request, f'Booking confirmed! Booking ID: {booking.booking_id}')
                    return redirect('bookings:my_bookings')
                else:
                    messages.error(request, 'Not enough seats available.')
    else:
        form = BookingForm(travel_option=travel)
    
    return render(request, 'bookings/book.html', {
        'travel': travel,
        'form': form
    })


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    current = bookings.filter(travel_option__date_time__gt=timezone.now())
    past = bookings.filter(travel_option__date_time__lte=timezone.now())
    
    return render(request, 'bookings/my_bookings.html', {
        'current_bookings': current,
        'past_bookings': past
    })


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.cancel():
        messages.success(request, 'Booking cancelled successfully.')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    
    return redirect('bookings:my_bookings')