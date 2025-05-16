from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Comment


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model with limited fields."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


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