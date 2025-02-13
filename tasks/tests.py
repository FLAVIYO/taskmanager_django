from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from .models import Task

class TaskTests(APITestCase):
    def setUp(self):
        # Create a regular user
        self.user = CustomUser.objects.create_user(
            email='user@example.com', password='testpass123', role='USER'
        )
        # Create an admin user
        self.admin = CustomUser.objects.create_user(
            email='admin@example.com', password='adminpass123', role='ADMIN'
        )
        # Create a task for the regular user
        self.task = Task.objects.create(
            user=self.user,
            title='Test Task',
            description='Test Description',
            due_date='2024-12-31T00:00:00Z',
            status='PENDING'
        )

    def get_token(self, email, password):
        # Helper function to get JWT token
        url = reverse('login')
        data = {'email': email, 'password': password}
        response = self.client.post(url, data, format='json')
        return response.data['access']

    def test_create_task(self):
        # Test task creation by a regular user
        token = self.get_token('user@example.com', 'testpass123')
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'due_date': '2024-12-31T00:00:00Z',
            'status': 'PENDING'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_retrieve_task(self):
        # Test retrieving a task by the owner
        token = self.get_token('user@example.com', 'testpass123')
        url = reverse('task-detail', args=[self.task.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Task')

    def test_update_task(self):
        # Test updating a task by the owner
        token = self.get_token('user@example.com', 'testpass123')
        url = reverse('task-detail', args=[self.task.id])
        data = {'title': 'Updated Task'}
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Task')

    def test_delete_task(self):
        # Test deleting a task by the owner
        token = self.get_token('user@example.com', 'testpass123')
        url = reverse('task-detail', args=[self.task.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_admin_access_all_tasks(self):
        # Test admin accessing all tasks
        token = self.get_token('admin@example.com', 'adminpass123')
        url = reverse('task-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should see the task created by the user

    def test_user_cannot_access_others_tasks(self):
        # Test user cannot access tasks created by others
        new_user = CustomUser.objects.create_user(
            email='user2@example.com', password='user2pass123', role='USER'
        )
        token = self.get_token('user2@example.com', 'user2pass123')
        url = reverse('task-detail', args=[self.task.id])
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)