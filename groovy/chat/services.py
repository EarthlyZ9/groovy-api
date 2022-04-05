from django.db.models import Q
from group.models import GroupMember, Group
from chat.models import PersonalChat, PersonalChatroom, GroupChatroom
from chat.serializers import PersonalChatroomSerializer, GroupChatroomSerializer


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
    def group_chatroom_list(user):
        # TODO: 내가 속해있는 그룹 채팅방 로드
        my_group = GroupMember.objects.filter(member=user).all()
        group_queryset = Group.objects
        for group in my_group.iterator():
            group_queryset |= Group.objects.filter(id=group.group_id).first()

        group_chat_queryset = GroupChatroom.objects
        for group in group_queryset.iterator():
            group_chat_queryset |= group.groupchatroom_set.all()
        group = GroupChatroomSerializer(group_chat_queryset)
        return group

    @staticmethod
    def personal_chatroom_list(user):
        personal_chat_queryset = PersonalChatroom.objects.filter(
            Q(sender=user) | Q(receiver=user)
        )
        return PersonalChatroomSerializer(personal_chat_queryset)
