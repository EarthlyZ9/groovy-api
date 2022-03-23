from django.contrib.auth import get_user_model
from rest_framework import serializers
from user.models import University

User = get_user_model()


class UniversitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = University
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "name", "created_at", "updated_at"]


class MiniUniversitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = University
        fields = ["url", "id", "name"]
        read_only_fields = ["url", "id", "name"]


class UserSerializer(serializers.HyperlinkedModelSerializer):

    university = MiniUniversitySerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "nickname",
            "gender",
            "university",
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
            "name",
            "gender"
            "admission_class",
            "profile_image_url",
            "thumbnail_image_url",
            "push_id",
            "login_attempt_at",
            "last_login_at",
            "auth_token",
            "is_service_terms_agreed",
            "is_deleted",
        ]


class SimplifiedUserSerializer(serializers.HyperlinkedModelSerializer):
    university_id = MiniUniversitySerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "email",
            "nickname",
            "university_id",
            "admission_class",
            "grade",
            "profile_image_url",
            "thumbnail_image_url",
        ]
        read_only_fields = [
            "url",
            "id",
            "email",
            "nickname",
            "university_id",
            "admission_class",
            "grade",
            "profile_image_url",
            "thumbnail_image_url",
        ]



