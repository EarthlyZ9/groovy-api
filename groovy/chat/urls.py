from django.urls import path

from .views import (
    GroupChatDetail,
    GroupChatroomList, PersonalChatroomList, GroupChatList, PersonalChatList,
    GroupChatroomNoticeDetail, GroupChatroomDetail, PersonalChatroomDetail, PersonalChatDetail,
)

urlpatterns = [
    path("group-chatrooms/", GroupChatroomList.as_view(), name="group-chatroom-list"),
    path("group-chatrooms/<int:pk>", GroupChatroomDetail.as_view(), name="group-chatroom-detail"),
    path("group-chatrooms/<int:pk>/notice/", GroupChatroomNoticeDetail.as_view(), name="group-chatroom-notice"),

    path("personal-chatrooms/", PersonalChatroomList.as_view(), name="personal-chatroom-list"),
    path("personal-chatrooms/<int:pk>", PersonalChatroomDetail.as_view(), name="personal-chatroom-list"),

    path("group-chatroom/<int:pk>/", GroupChatList.as_view(), name="group-chat-list"),
    path("personal-chatroom/<int:pk>/", PersonalChatList.as_view(), name="personal-chat-list"),

    path("group-chats/<int:pk>", GroupChatDetail.as_view(), name="group-chat-detail"),
    path("personal-chats/<int:pk>", PersonalChatDetail.as_view(), name="personal-chat-detail"),
]
