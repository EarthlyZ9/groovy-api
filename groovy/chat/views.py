from rest_framework import generics, permissions, status
from rest_framework.response import Response
from chat.services import ChatService


class ChatRoomList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        personal = ChatService.personal_chatroom_list(user)
        group = ChatService.group_chatroom_list(user)
        return Response(
            {"personal": personal, "group": group}, status=status.HTTP_200_OK
        )

    # TODO: 채팅방 나가기 기능 더하기


class GroupChatDetail(generics.ListCreateAPIView):
    # TODO: 채팅 불러오기
    pass


class PersonalChatDetail(generics.ListCreateAPIView):
    pass
