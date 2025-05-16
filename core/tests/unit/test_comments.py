from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from core.models import Task
from rest_framework_simplejwt.tokens import RefreshToken

class CommentUnitTestCase(APITestCase):
    def setUp(self):
        # Create user and authenticate
        self.user = User.objects.create_user(username='commenter', password='password123')
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

        # Create a task instance for comment relation
        self.task = Task.objects.create(
            title="Sample Task",
            description="Sample Description",
            status="Not Started",
            priority="Medium",
        )

    def test_create_comment(self):
        data = {
            "task": self.task.id,
            "content": "This is a test comment."
        }
        response = self.client.post("/api/comments/", data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Comment is successfully created")
