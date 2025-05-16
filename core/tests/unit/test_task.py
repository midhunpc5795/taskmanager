"""
Unit tests for Task CRUD operations.
These tests ensure that the Task API endpoints are functioning correctly in isolation.
"""

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from core.models import Task
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class TaskUnitTestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')

        # Create API client instance
        self.client = APIClient()

        # Generate JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Set Authorization header for all requests made with this client
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_task(self):
        data = {
            "title": "Test Task",
            "description": "A test task.",
            "status": "Not Started",
            "priority": "Medium"
        }
        response = self.client.post("/api/tasks/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

    def test_update_task(self):
        task = Task.objects.create(
            title="Initial Title",
            description="Initial desc",
            status="Not Started",
            priority="Low"
        )
        task.assigned_users.add(self.user)
        response = self.client.put(f"/api/tasks/{task.id}/", {
            "title": "Updated Title",
            "description": "Updated desc",
            "status": "In Progress",
            "priority": "High"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Task is successfully updated")