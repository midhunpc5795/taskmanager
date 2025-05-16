from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with limited fields."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    Includes two password fields to ensure password confirmation.
    Validates that both passwords match before creating the user.
    """

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def validate(self, data):
        """
        Validate that password1 and password2 are the same.

        Raises:
            serializers.ValidationError: If the two passwords do not match.
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Create and return a new User instance, after hashing the password.

        Args:
            validated_data (dict): Validated data from serializer.

        Returns:
            User: Newly created User instance.
        """
        username = validated_data['username']
        email = validated_data.get('email')
        password = validated_data['password1']

        user = User(username=username, email=email)
        user.set_password(password)  # Hash the password properly
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer to include additional user info
    and a success message in the token response.
    """

    def validate(self, attrs):
        """
        Validate user credentials and generate tokens.

        Adds extra data to the response, including a success message
        and user information (username and email).

        Args:
            attrs (dict): Credentials passed for validation.

        Returns:
            dict: Token data along with additional user info.
        """
        data = super().validate(attrs)

        # Add extra response data
        data.update({
            'message': 'User logged in successfully',
            'user': {
                'username': self.user.username,
                'email': self.user.email,
            }
        })
        return data

class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model with read-only user and timestamp fields."""

    class Meta:
        model = Comment
        fields = ['id', 'content', 'timestamp', 'task', 'user']
        read_only_fields = ['user', 'timestamp']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model including assigned users and related comments."""
    
    assigned_users = UserSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'