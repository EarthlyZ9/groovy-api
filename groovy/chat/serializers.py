from rest_framework import serializers
from chat.models import GroupChatroom, GroupChat, RegularChat
from group.serializers import GroupSerializer
from user.serializers import SimplifiedUserSerializer


class GroupChatroomSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GroupChatroom
        fields = [
            "url",
            "id",
            "group_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "url",
            "id",
            "group_id",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            'url': {'view_name': 'group-chatroom-detail'},
        }


class GroupChatSerializer(serializers.HyperlinkedModelSerializer):
    chatroom_id = GroupChatroomSerializer(read_only=True)
    user_id = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = GroupChat
        fields = [
            "id",
            "chatroom_id",
            "user_id",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "chatroom_id",
            "user_id",
            "content",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            'url': {'view_name': 'group-chat-detail'},
        }


class RegularChatSerializer(serializers.HyperlinkedModelSerializer):
    sender = SimplifiedUserSerializer(read_only=True)
    receiver = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = RegularChat
        fields = [
            "id",
            "sender",
            "receiver",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "sender",
            "receiver",
            "content",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            'url': {'view_name': 'regular-chat-detail'},
        }