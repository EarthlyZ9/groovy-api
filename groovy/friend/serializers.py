from rest_framework import serializers
from user.serializers import SimplifiedUserSerializer
from friend.models import Friend, FriendRequest


class FriendSerializer(serializers.HyperlinkedModelSerializer):
    user_id = SimplifiedUserSerializer(read_only=True)
    friend_id = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = [
            "url",
            "id",
            "user_id",
            "friend_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "url",
            "id",
            "user_id",
            "friend_id",
            "created_at",
            "updated_at",
        ]


class FriendRequestSerializer(serializers.HyperlinkedModelSerializer):
    request_from = SimplifiedUserSerializer(read_only=True)
    request_to = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = [
            "url",
            "id",
            "request_from",
            "request_to",
            "status",
            "status_changed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "url",
            "id",
            "request_from",
            "request_to",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            'url': {'view_name': 'friend-request-detail'},
        }

