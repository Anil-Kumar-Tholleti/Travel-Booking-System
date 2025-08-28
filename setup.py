#!/usr/bin/env python3
"""
Travel Booking Application Setup Script

This script helps set up the Travel Booking application for development.
Run this script after installing requirements and configuring your database.
"""

import os
import sys
import django
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_booking.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from django.db import connection


def check_database():
    """Check if database is accessible."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def run_migrations():
    """Run database migrations."""
    try:
        print("🔄 Running database migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False


def create_superuser():
    """Create a superuser if none exists."""
    try:
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superuser already exists")
            return True
        
        print("👤 Creating superuser...")
        print("Please provide superuser details:")
        
        username = input("Username (admin): ").strip() or "admin"
        email = input("Email (admin@example.com): ").strip() or "admin@example.com"
        
        while True:
            password = input("Password: ").strip()
            if len(password) >= 8:
                break
            print("Password must be at least 8 characters long")
        
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser '{username}' created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False


def load_sample_data():
    """Load sample travel data."""
    try:
        response = input("Load sample travel data? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            print("📊 Loading sample data...")
            execute_from_command_line(['manage.py', 'load_sample_data'])
            print("✅ Sample data loaded successfully")
        else:
            print("⏭️  Skipping sample data loading")
        return True
    except Exception as e:
        print(f"❌ Sample data loading failed: {e}")
        return False


def collect_static():
    """Collect static files."""
    try:
        print("📁 Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Static files collected successfully")
        return True
    except Exception as e:
        print(f"❌ Static files collection failed: {e}")
        return False


def main():
    """Main setup function."""
    print("🚀 Travel Booking Application Setup")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = project_root / '.env'
    if not env_file.exists():
        print("⚠️  .env file not found!")
        print("Please create a .env file with your configuration.")
        print("You can copy .env.example and modify it for your needs.")
        return
    
    steps = [
        ("Database Connection", check_database),
        ("Database Migrations", run_migrations),
        ("Superuser Creation", create_superuser),
        ("Sample Data Loading", load_sample_data),
        ("Static Files Collection", collect_static),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}")
        print("-" * 30)
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000")
    print("3. Admin panel: http://127.0.0.1:8000/admin")
    print("\nHappy coding! 🚀")


if __name__ == "__main__":
    main()
