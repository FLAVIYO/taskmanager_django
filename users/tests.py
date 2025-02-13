from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser

class UserTests(APITestCase):
    def setUp(self):
        # Create a regular user
        self.user = CustomUser.objects.create_user(
            email='user@example.com', password='testpass123', role='USER'
        )
        # Create an admin user
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com', password='adminpass123', role='ADMIN'
        )

    def test_user_signup(self):
        # Test user signup
        url = reverse('signup')
        data = {
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'role': 'USER'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 3)

    def test_user_login(self):
        # Test user login
        url = reverse('login')
        data = {'email': 'user@example.com', 'password': 'testpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_admin_login(self):
        # Test admin login
        url = reverse('login')
        data = {'email': 'admin@example.com', 'password': 'adminpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)