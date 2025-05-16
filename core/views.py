from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://localhost:8000/'

    def post(self, request, *args, **kwargs):
        print("POST data received:", request.data)  # Log the POST data
        return super().post(request, *args, **kwargs)

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Task CRUD operations with custom response messages.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Create a new Task instance.
        """
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Task is successfully created", "data": response.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """
        Update an existing Task instance.
        """
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Task is successfully updated", "data": response.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a Task instance.
        """
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Task is successfully deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Comment CRUD operations with custom response messages.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the Comment with the current authenticated user.
        """
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new Comment instance.
        """
        response = super().create(request, *args, **kwargs)
        return Response(
            {"message": "Comment is successfully created", "data": response.data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """
        Update an existing Comment instance.
        """
        response = super().update(request, *args, **kwargs)
        return Response(
            {"message": "Comment is successfully updated", "data": response.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a Comment instance.
        """
        super().destroy(request, *args, **kwargs)
        return Response(
            {"message": "Comment is successfully deleted"},
            status=status.HTTP_204_NO_CONTENT
        )
