from rest_framework import generics
from chat.models import GroupChatroom, GroupChat, RegularChat
from chat.serializers import GroupChatroomSerializer, GroupChatSerializer, RegularChatSerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response


class ChatApiRoot(generics.GenericAPIView):
    name = 'Chat'

    def get(self, request, *args, **kwargs):
        return Response({
            'group_chatroom': reverse('group-chatroom-list', request=request),
            'group_chat': reverse('group-chat-list', request=request),
            'regular_chat': reverse('regular-chat-list', request=request),
            })


class GroupChatroomList(generics.ListCreateAPIView):
    queryset = GroupChatroom.objects.all()
    serializer_class = GroupChatroomSerializer


class GroupChatroomDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupChatroom.objects.all()
    serializer_class = GroupChatroomSerializer


class GroupChatList(generics.ListCreateAPIView):
    queryset = GroupChat.objects.all().order_by('chatroom_id')
    serializer_class = GroupChatSerializer


class GroupChatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupChatroom.objects.all()
    serializer_class = GroupChatSerializer


class RegularChatList(generics.ListCreateAPIView):
    queryset = RegularChat.objects.all().order_by('receiver_id')
    serializer_class = RegularChatSerializer


class RegularChatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegularChat.objects.all()
    serializer_class = RegularChatSerializer
