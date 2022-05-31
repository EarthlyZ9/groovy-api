from django.db.models import Q

from chat.models import PersonalChat, PersonalChatroom, GroupChatroom, GroupChat
from chat.serializers import PersonalChatroomSerializer
from group.models import Group


class ChatService:
    @staticmethod
    def join_request_chat(requestor, group):
        content = f"'{group.title}' 그룹에 쪼인하고 싶어요!"
        return PersonalChat.objects.create(
            sender=requestor,
            receiver_id=group.manager_id,
            content=content,
            is_join_request_message=True,
        )

    @staticmethod
    def get_group_chatroom_queryset(user):
        group_queryset = Group.objects.filter(members=user)
        group_chatroom_queryset = GroupChatroom.objects.none()
        for instance in group_queryset:
            group_chatroom_queryset |= instance.group_chatroom
        group_chatroom_queryset = group_chatroom_queryset.order_by('updated_at')
        return group_chatroom_queryset

    # TODO: Test with Datagrip (dummy data)

    @staticmethod
    def get_personal_chatroom_queryset(user):
        personal_chat_queryset = PersonalChatroom.objects.filter(
            Q(sender=user) | Q(receiver=user)
        )
        return PersonalChatroomSerializer(personal_chat_queryset)

    @staticmethod
    def get_all_group_chats(chatroom_id):
        return GroupChat.objects.all_with_deleted().filter(id=chatroom_id).order_by('-created_at')

    @staticmethod
    def get_all_personal_chats(chatroom_id):
        return PersonalChat.objects.all_with_deleted().filter(id=chatroom_id).order_by('-created_at')

    @staticmethod
    def delete_notice(obj):
        obj.pinned_chat = None
        return obj

    @staticmethod
    def create_group_chatroom(group):
        return GroupChatroom.objects.create(group=group)
