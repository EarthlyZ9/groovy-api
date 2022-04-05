from rest_framework import serializers
from chat.models import GroupChatroom, GroupChat, PersonalChatroom, PersonalChat
from group.serializers import GroupSerializer, MiniGroupSerializer
from user.serializers import SimplifiedUserSerializer


class GroupChatroomSerializer(serializers.ModelSerializer):
    group = MiniGroupSerializer(read_only=True)
    latest_chat = serializers.SerializerMethodField()

    class Meta:
        model = GroupChatroom
        fields = [
            "id",
            "group",
            "latest_chat",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "group",
            "latest_chat",
            "created_at",
            "updated_at",
        ]

    def get_latest_chat(self, obj):
        instance = (
            GroupChat.objects.filter(chatroom_id=obj.id).order_by("created_at").first()
        )
        return GroupChatSerializer(instance)


class GroupChatSerializer(serializers.ModelSerializer):
    chatroom = GroupChatroomSerializer(read_only=True)
    user = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = GroupChat
        fields = [
            "id",
            "chatroom",
            "user",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "chatroom",
            "user",
            "content",
            "created_at",
            "updated_at",
        ]


class PersonalChatroomSerializer(serializers.ModelSerializer):
    group = MiniGroupSerializer(read_only=True)
    latest_chat = serializers.SerializerMethodField()

    class Meta:
        model = PersonalChatroom
        fields = [
            "id",
            "sender",
            "receiver",
            "latest_chat",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "sender",
            "receiver",
            "latest_chat",
            "created_at",
            "updated_at",
        ]

    def get_latest_chat(self, obj):
        instance = (
            PersonalChat.objects.filter(chatroom_id=obj.id)
            .order_by("created_at")
            .first()
        )
        return PersonalChatroomSerializer(instance)


class PersonalChatSerializer(serializers.ModelSerializer):
    chatroom = PersonalChatroomSerializer(read_only=True)
    sender = SimplifiedUserSerializer(read_only=True)
    receiver = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = PersonalChat
        fields = [
            "id",
            "chatroom",
            "sender",
            "receiver",
            "content",
            "is_join_request",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "chatroom",
            "sender",
            "receiver",
            "content",
            "is_join_request",
            "created_at",
            "updated_at",
        ]
