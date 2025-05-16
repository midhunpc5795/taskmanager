import requests

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .models import Task, Comment
from .serializers import (
    TaskSerializer,
    CommentSerializer,
    RegisterSerializer,
    MyTokenObtainPairSerializer,
)

GITHUB_CLIENT_ID = settings.GITHUB_CLIENT_ID
GITHUB_CLIENT_SECRET = settings.GITHUB_CLIENT_SECRET

@api_view(['POST'])
def github_auth(request):
    """
        Handle GitHub OAuth authentication.

        Expects a 'code' in the POST request data, which is the authorization code
        obtained from GitHub OAuth flow.

        Steps:
        1. Exchange the authorization code for an access token from GitHub.
        2. Retrieve the GitHub user's profile information using the access token.
        3. Get or create a Django User corresponding to the GitHub user.
        4. Issue JWT refresh and access tokens for the user.

        Returns:
            200 OK with JWT tokens and user info on success,
            400 Bad Request with error message on failure.

        # Note: This GitHub OAuth authentication does NOT return the user's GitHub password.
        # You should send a separate set-password or password-reset link to the user
        # if you want them to be able to log in with username/password in your system.
    """
    code = request.data.get('code')
    if not code:
        return Response({'error': 'Code not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Exchange authorization code for access token from GitHub
    token_url = 'https://github.com/login/oauth/access_token'
    token_data = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code,
    }
    headers = {'Accept': 'application/json'}
    token_response = requests.post(token_url, data=token_data, headers=headers)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if not access_token:
        return Response({'error': 'Failed to get access token'}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve user info from GitHub API using access token
    user_url = 'https://api.github.com/user'
    user_headers = {'Authorization': f'token {access_token}'}
    user_response = requests.get(user_url, headers=user_headers)
    user_data = user_response.json()

    if 'id' not in user_data:
        return Response({'error': 'Failed to fetch user info'}, status=status.HTTP_400_BAD_REQUEST)

    # Use GitHub login as username and email if available
    username = user_data.get('login')
    email = user_data.get('email') or f'{username}@github.com'  # fallback email if GitHub email is private

    # Get or create the user in the Django database
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})

    # Generate JWT refresh and access tokens for the user
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': {
            'username': user.username,
            'email': user.email,
        }
    })


class RegisterView(generics.CreateAPIView):
    """
    API endpoint for user registration.

    Accepts user registration data, validates it using RegisterSerializer,
    creates a new user, and returns JWT refresh and access tokens
    along with user information on successful registration.
    """
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens upon successful registration
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_201_CREATED)


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to obtain JWT token pair (access and refresh).

    Uses a custom serializer (MyTokenObtainPairSerializer) to validate
    user credentials and issue JWT tokens.
    """
    serializer_class = MyTokenObtainPairSerializer

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/auth/google/callback/"
    client_class = OAuth2Client

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
