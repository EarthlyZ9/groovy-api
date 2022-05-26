from rest_framework import generics, status

from chat.models import GroupChatroomNotice, GroupChat, \
    GroupChatroom, PersonalChatroom, PersonalChat
from chat.permissions import IsGroupChatOwnerOrReadOnly, IsPersonalChatOwnerOrReadOnly
from chat.serializers import PersonalChatroomSerializer, GroupChatroomSerializer, GroupChatSerializer, \
    PersonalChatSerializer, GroupChatroomNoticeSerializer
from chat.services import ChatService
from config.Response import Response
from group.services import GroupService


class GroupChatroomList(generics.ListAPIView):
    serializer_class = GroupChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ChatService.get_group_chatroom_queryset(user).order_by('updated_at')
        return queryset


class GroupChatroomDetail(generics.RetrieveDestroyAPIView):
    """
    get(retrieve): 채팅방 정보 (id, group, latest_chat, notice, created_at, update_at)
    delete: 채팅방 (그룹) 나가기
    """
    queryset = GroupChatroom.objects.all()
    serializer_class = GroupChatroomSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        group = instance.group
        deleted = GroupService.delete_group_member(group, request.user)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)


class GroupChatroomNoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupChatroomNoticeSerializer
    queryset = GroupChatroomNotice.objects.all()

    def retrieve(self, request, *args, **kwargs):
        chatroom_id = kwargs.get("pk")
        instance = GroupChatroomNotice.objects.filter(chatroom_id=chatroom_id).first()

        return Response(data=GroupChatroomNoticeSerializer(instance).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        chatroom_id = kwargs.get("pk")
        instance = GroupChatroomNotice.objects.filter(chatroom_id=chatroom_id).first()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(data=serializer.data)

    def delete(self, request, *args, **kwargs):
        chatroom_id = kwargs.get("pk")
        instance = GroupChatroomNotice.objects.filter(chatroom_id=chatroom_id).first()

        return Response(data=GroupChatroomNoticeSerializer(ChatService.delete_notice(instance)).data)


class PersonalChatroomList(generics.ListAPIView):
    serializer_class = PersonalChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ChatService.get_personal_chatroom_queryset(user).order_by('updated_at')
        return queryset


class PersonalChatroomDetail(generics.RetrieveDestroyAPIView):
    """
    get(retrieve): 개인 채팅방 정보
    delete: 채팅방 (그룹) 나가기
    """
    queryset = PersonalChatroom.objects.all()
    serializer_class = PersonalChatroomSerializer


class GroupChatList(generics.ListCreateAPIView):
    serializer_class = GroupChatSerializer

    def get_queryset(self):
        chatroom_id = self.kwargs.get('pk')
        queryset = ChatService.get_all_group_chats(chatroom_id=chatroom_id)
        return queryset

    def perform_create(self, serializer):
        chatroom_id = self.kwargs.get("pk")
        serializer.save(user=self.request.user, chatroom_id=chatroom_id)


class PersonalChatList(generics.ListCreateAPIView):
    serializer_class = PersonalChatSerializer

    def get_queryset(self):
        chatroom_id = self.kwargs.get('pk')
        queryset = ChatService.get_all_personal_chats(chatroom_id=chatroom_id)
        return queryset

    def perform_create(self, serializer):
        chatroom_id = self.kwargs.get("pk")
        serializer.save(sender=self.request.user, chatroom_id=chatroom_id)


class GroupChatDetail(generics.DestroyAPIView):
    serializer_class = GroupChatSerializer
    permission_classes = [IsGroupChatOwnerOrReadOnly]
    queryset = GroupChat.objects.all()


class PersonalChatDetail(generics.DestroyAPIView):
    serializer_class = PersonalChatSerializer
    permission_classes = [IsPersonalChatOwnerOrReadOnly]
    queryset = PersonalChat.objects.all()
