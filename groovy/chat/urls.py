from django.urls import path

from .views import (
    GroupChatDetail,
    PersonalChatDetail, GroupChatroomList, PersonalChatroomList, GroupChatList, PersonalChatList,
    GroupChatroomNoticeDetail, PersonalChatroomNoticeDetail,
)

urlpatterns = [
    path("", GroupChatroomList.as_view(), name="group_chatroom_list"),
    path("personal/", PersonalChatroomList.as_view(), name="personal_chatroom_list"),

    path("<int:pk>/", GroupChatList.as_view(), name="group_chat_list"),
    path("personal/<int:pk>/", PersonalChatList.as_view(), name="personal_chat_list"),

    path("<int:pk>/notice/", GroupChatroomNoticeDetail.as_view(), name="group_chat_notice"),
    path("personal/<int:pk>/notice/", PersonalChatroomNoticeDetail.as_view(), name="personal_chat_notice"),

    path("<int:pk>/chat/<int:chat_id>", PersonalChatDetail.as_view(), name="group_chat_detail"),
    path("personal/<int:pk>/chat/<int:chat_id>", GroupChatDetail.as_view(), name="personal_chat_detail"),
]
