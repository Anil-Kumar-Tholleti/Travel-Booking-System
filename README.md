# Travel Booking - Clean Django 5 Project

A minimal, clean Django 5 travel booking application with user management and booking functionality.

## Features

### 🔐 User Management (accounts app)
- User registration with profile creation
- Login/logout functionality  
- Profile update (name, email, phone, address)

### ✈️ Travel Booking (bookings app)
- Browse travel options (Flight, Train, Bus)
- Advanced filtering (type, source, destination, date)
- Book travel with seat validation
- View and cancel bookings
- Admin interface for managing travel options

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Add Sample Data (Optional)
```bash
python manage.py shell -c "
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from bookings.models import TravelOption

TravelOption.objects.create(
    type='FLIGHT', source='New York', destination='Los Angeles',
    date_time=timezone.now() + timedelta(days=7),
    price=Decimal('299.99'), available_seats=50
)

TravelOption.objects.create(
    type='TRAIN', source='Chicago', destination='Denver', 
    date_time=timezone.now() + timedelta(days=5),
    price=Decimal('89.99'), available_seats=80
)

TravelOption.objects.create(
    type='BUS', source='Miami', destination='Orlando',
    date_time=timezone.now() + timedelta(days=3), 
    price=Decimal('25.99'), available_seats=35
)
"
```

### 5. Run Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Database Configuration

### SQLite (Default)
No configuration needed - uses `db.sqlite3`

### MySQL (Optional)
Create `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

USE_MYSQL=True
DB_NAME=travel_booking
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

## Project Structure

```
travel_booking/
├── accounts/           # User management
│   ├── models.py      # User Profile model
│   ├── forms.py       # Registration & profile forms  
│   ├── views.py       # Auth views
│   └── urls.py        # Account URLs
├── bookings/          # Travel booking
│   ├── models.py      # TravelOption & Booking models
│   ├── forms.py       # Booking & filter forms
│   ├── views.py       # Booking logic
│   └── urls.py        # Booking URLs  
├── templates/         # Bootstrap templates
│   ├── base.html      # Base template
│   ├── accounts/      # Auth templates
│   └── bookings/      # Booking templates
└── travel_booking/    # Django settings
    ├── settings.py    # Project settings
    └── urls.py        # Main URLs
```

## Models

### User Profile (accounts.Profile)
- `user`: OneToOneField(User)
- `phone`: CharField (optional)
- `address`: TextField (optional)

### Travel Option (bookings.TravelOption) 
- `id`: UUIDField (primary key)
- `type`: CharField (FLIGHT/TRAIN/BUS)
- `source/destination`: CharField
- `date_time`: DateTimeField  
- `price`: DecimalField
- `available_seats`: PositiveIntegerField

### Booking (bookings.Booking)
- `id`: UUIDField (primary key)
- `user`: ForeignKey(User)
- `travel_option`: ForeignKey(TravelOption)
- `seats`: PositiveIntegerField
- `total_price`: DecimalField (auto-calculated)
- `status`: CharField (CONFIRMED/CANCELLED)

## URLs

- `/` - Travel list with filters
- `/book/<uuid>/` - Book travel option
- `/my-bookings/` - User's bookings
- `/cancel/<uuid>/` - Cancel booking
- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/profile/` - User profile
- `/admin/` - Admin interface

## Admin Interface

Access at `/admin/` to:
- Manage travel options
- View bookings
- Manage users

## Requirements

- Python 3.8+
- Django 5.0+
- Bootstrap 5.3 (CDN)
- SQLite (default) or MySQL

## Clean & Minimal

This project focuses on:
- ✅ Essential functionality only
- ✅ Clean, readable code
- ✅ Minimal dependencies
- ✅ Bootstrap styling
- ✅ Ready to run after `migrate`
- ✅ Proper form validation
- ✅ Atomic booking transactions
## 🔖 Languages Used
![Python](https://img.shields.io/badge/Python-61.8%25-blue?logo=python)
![HTML](https://img.shields.io/badge/HTML-32.5%25-orange?logo=html5)
![CSS](https://img.shields.io/badge/CSS-5.7%25-purple?logo=css3)
