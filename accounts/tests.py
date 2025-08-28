from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile


class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_profile_creation_signal(self):
        """Test that Profile is automatically created when User is created."""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)

    def test_user_registration(self):
        """Test user registration functionality."""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        """Test user login functionality."""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login

    def test_profile_update(self):
        """Test profile update functionality."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('accounts:profile'), {
            'username': 'testuser',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'phone': '1234567890',
            'address': '123 Test St'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        
        # Check if profile was updated
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.profile.phone, '1234567890')
