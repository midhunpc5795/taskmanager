from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from core.models import Task, Comment
from rest_framework_simplejwt.tokens import RefreshToken

class MultiUserInteractionTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="alicepass")
        self.user2 = User.objects.create_user(username="bob", password="bobpass")
        self.task = Task.objects.create(title="Shared Task", description="desc", status="Not Started", priority="Medium")

        # Create API clients for each user with JWT auth
        self.client1 = APIClient()
        self.client2 = APIClient()

        refresh1 = RefreshToken.for_user(self.user1)
        refresh2 = RefreshToken.for_user(self.user2)

        self.client1.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh1.access_token)}')
        self.client2.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh2.access_token)}')

    def test_multiple_users_commenting(self):
        # User1 posts comment
        response1 = self.client1.post("/api/comments/", {"task": self.task.id, "content": "Alice's comment"})
        self.assertEqual(response1.status_code, 201)

        # User2 posts comment
        response2 = self.client2.post("/api/comments/", {"task": self.task.id, "content": "Bob's comment"})
        self.assertEqual(response2.status_code, 201)

        comments = Comment.objects.filter(task=self.task)
        self.assertEqual(comments.count(), 2)
        self.assertTrue(comments.filter(content__icontains="Alice").exists())
        self.assertTrue(comments.filter(content__icontains="Bob").exists())
