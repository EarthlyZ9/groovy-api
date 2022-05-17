from django.urls import path

from .views import (
    GroupChatDetail,
    PersonalChatDetail, GroupChatroomList, PersonalChatroomList, GroupChatList, PersonalChatList,
    GroupChatroomNoticeDetail, PersonalChatroomNoticeDetail,
)

urlpatterns = [
    path("", GroupChatroomList.as_view(), name="group-chatroom-list"),
    path("personal/", PersonalChatroomList.as_view(), name="personal-chatroom-list"),

    path("<int:pk>/", GroupChatList.as_view(), name="group-chat-list"),
    path("personal/<int:pk>/", PersonalChatList.as_view(), name="personal-chat-list"),

    path("<int:pk>/notice/", GroupChatroomNoticeDetail.as_view(), name="group-chat-notice"),
    path("personal/<int:pk>/notice/", PersonalChatroomNoticeDetail.as_view(), name="personal-chat-notice"),

    path("<int:pk>/chat/<int:chat_id>", PersonalChatDetail.as_view(), name="group-chat-detail"),
    path("personal/<int:pk>/chat/<int:chat_id>", GroupChatDetail.as_view(), name="personal-chat-detail"),
]
