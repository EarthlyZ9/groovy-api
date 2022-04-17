from rest_framework import generics

from chat.models import GroupChatroomNotice, PersonalChatroomNotice, GroupChat, \
    PersonalChat
from chat.serializers import PersonalChatroomSerializer, GroupChatroomSerializer, GroupChatSerializer, \
    PersonalChatSerializer, GroupChatroomNoticeSerializer, PersonalChatroomNoticeSerializer
from chat.services import ChatService
from config.Response import Response


class GroupChatroomList(generics.ListAPIView):
    serializer_class = GroupChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ChatService.get_group_chatroom_queryset(user).order_by('updated_at')
        return queryset


class GroupChatroomNoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupChatroomNoticeSerializer
    queryset = GroupChatroomNotice.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(data=GroupChatroomNoticeSerializer(ChatService.delete_notice(instance)).data)


class PersonalChatroomNoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PersonalChatroomNoticeSerializer
    queryset = PersonalChatroomNotice.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(data=PersonalChatroomNoticeSerializer(ChatService.delete_notice(instance)).data)


class PersonalChatroomList(generics.ListAPIView):
    serializer_class = PersonalChatroomSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = ChatService.get_personal_chatroom_queryset(user).order_by('updated_at')
        return queryset


class GroupChatList(generics.ListCreateAPIView):
    serializer_class = GroupChatSerializer

    def get_queryset(self):
        chatroom_id = self.kwargs.get('pk')
        queryset = ChatService.get_all_group_chats(chatroom_id=chatroom_id)
        return queryset


class PersonalChatList(generics.ListCreateAPIView):
    serializer_class = PersonalChatSerializer

    def get_queryset(self):
        chatroom_id = self.kwargs.get('pk')
        queryset = ChatService.get_all_personal_chats(chatroom_id=chatroom_id)
        return queryset


class GroupChatDetail(generics.DestroyAPIView):
    serializer_class = GroupChatSerializer

    def get_queryset(self):
        chat_id = self.kwargs.get("chat_id")
        return GroupChat.objects.filter(id=chat_id)


class PersonalChatDetail(generics.DestroyAPIView):
    serializer_class = PersonalChatSerializer

    def get_queryset(self):
        chat_id = self.kwargs.get("chat_id")
        return PersonalChat.objects.filter(id=chat_id)
