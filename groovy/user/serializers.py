from django.contrib.auth import get_user_model
from rest_framework import serializers
from user.models import University

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer class for User model.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "nickname",
            "gender"
            "university_id",
            "is_university_confirmed",
            "university_confirmed_at",
            "admission_class",
            "grade",
            "profile_image_url",
            "thumbnail_image_url",
            "is_push_allowed",
            "push_id",
            "login_attempt_at",
            "last_login_at",
            "auth_token",
            "is_service_terms_agreed",
            "is_deleted",
        ]
        # api 로 get 만 할 필드
        read_only_fields = [
            "id",
            "email",
            "name",
            "gender"
            "admission_class",
            "grade",
            "profile_image_url",
            "thumbnail_image_url",
            "push_id",
            "login_attempt_at",
            "last_login_at",
            "auth_token",
            "is_service_terms_agreed",
            "is_deleted",
        ]


class MiniUserSerializer(serializers.ModelSerializer):
    """
    mini-Serializer class for short description of User.
    """

    class Meta:
        model = User
        fields = ["id", "email", "name", "nickname"]
        read_only_fields = ["id", "email", "name", "nickname"]


class UniversitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = University
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]