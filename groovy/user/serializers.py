from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.models import University, UniversityManualVerification

User = get_user_model()


class UniversitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "name", "created_at", "updated_at"]


class MiniUniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name"]
        read_only_fields = ["id", "name"]


class UserSerializer(serializers.ModelSerializer):
    university = MiniUniversitySerializer(read_only=True)
    bookmarks = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="group-bookmark-detail"
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "nickname",
            "gender",
            "university",
            "is_university_confirmed",
            "university_confirmed_at",
            "admission_class",
            "grade",
            "bookmarks",
            "profile_image_url",
            "thumbnail_image_url",
            "login_attempt_at",
            "last_login_at",
            "auth_token",
            "is_service_terms_agreed",
            "is_push_allowed",
            "push_id",
            "is_deleted",
            "created_at",
            "updated_at",
        ]
        # api 로 get 만 할 필드
        read_only_fields = [
            "id",
            "nickname",
            "gender",
            "university_confirmed_at",
            "bookmarks",
            "login_attempt_at",
            "last_login_at",
            "auth_token",
            "is_service_terms_agreed",
            "is_push_allowed",
            "push_id",
            "is_deleted",
            "created_at",
            "updated_at",
        ]


class SimplifiedUserSerializer(serializers.ModelSerializer):
    university = MiniUniversitySerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "nickname",
            "university",
            "admission_class",
            "grade",
            "profile_image_url",
            "thumbnail_image_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "email",
            "nickname",
            "university",
            "admission_class",
            "grade",
            "profile_image_url",
            "thumbnail_image_url",
            "created_at",
            "updated_at",
        ]


class UniversityVerificationSerializer(serializers.ModelSerializer):
    university = MiniUniversitySerializer(read_only=True)
    user = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = UniversityManualVerification
        fields = [
            "id",
            "user",
            "university",
            "verification_method",
            "verification_img_url",
            "verification_status",
            "status_changed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "university",
            "verification_method",
            "verification_img_url",
            "status_changed_at",
            "created_at",
            "updated_at",
        ]
