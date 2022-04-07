from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from friend.models import Friend
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
    bookmarks = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="group-bookmark-detail"
    )

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
            "bookmarks",
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
            "gender" "admission_class",
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
    university = MiniUniversitySerializer(read_only=True)
    is_friend = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "email",
            "nickname",
            "university",
            "admission_class",
            "grade",
            "profile_image_url",
            "thumbnail_image_url",
            "is_friend",
        ]
        read_only_fields = [
            "url",
            "id",
            "email",
            "nickname",
            "university",
            "admission_class",
            "grade",
            "profile_image_url",
            "thumbnail_image_url",
            "is_friend",
        ]

    def get_is_friend(self, obj):
        user = CurrentUserDefault()
        friend = Friend.objects.filter(user=user, friend_id=obj.id).first()
        if friend:
            return True
        else:
            return False
