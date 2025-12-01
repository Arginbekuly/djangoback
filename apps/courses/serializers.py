from typing import Any, Optional
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from apps.auths.models import CustomUser
from apps.courses.models import Courses, Lesson


class CoursesSerializer(serializers.ModelSerializer):
    """Course serializer"""
    owner = serializers.StringRelatedField()
    lessons_count = serializers.IntegerField(source='lessons_count', read_only=True)

    class Meta:
        model = Courses
        fields = ['title', 'description', 'is_active', 'owner', 'lessons_count', 'created_at', 'updated_at']


class LessonSerializer(serializers.ModelSerializer):
    """Lesson serializer"""

    class Meta:
        model = Lesson
        fields = ['course', 'title', 'content', 'order', 'indentation', 'is_published', 'created_at', 'updated_at']


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField(
        required=True,
        max_length=CustomUser.EMAIL_MAX_LENGTH,
    )
    password = serializers.CharField(
        required=True,
        max_length=CustomUser.PASSWORD_MAX_LENGTH,
        write_only=True,
    )

    def validate_email(self, value: str):
        """Validates the email field"""
        return value.lower()

    def validate(self, attrs: dict[str, Any]):
        """Validate the input data"""
        email: str = attrs["email"]
        password: str = attrs["password"]

        user: Optional[CustomUser] = CustomUser.objects.filter(email=email).first()

        if not user:
            raise ValidationError({
                "email": [f"User with email '{email}' doesn't exist"]
            })

        if not user.check_password(password):
            raise ValidationError({
                "password": ["Incorrect password"]
            })

        attrs["user"] = user
        return attrs
