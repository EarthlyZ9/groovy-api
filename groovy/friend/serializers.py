from rest_framework import serializers

from friend.models import Friend, FriendRequest
from user.serializers import SimplifiedUserSerializer


class FriendSerializer(serializers.ModelSerializer):
    friend = SimplifiedUserSerializer(read_only=True, many=True)

    class Meta:
        model = Friend
        fields = [
            "id",
            "user",
            "friend",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user_id",
            "friend_id",
            "created_at",
            "updated_at",
        ]


class FriendRequestSerializer(serializers.ModelSerializer):
    request_from = SimplifiedUserSerializer(read_only=True)
    request_to = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = [
            "id",
            "request_from",
            "request_to",
            "status",
            "status_changed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "request_from",
            "request_to",
            "created_at",
            "updated_at",
        ]
