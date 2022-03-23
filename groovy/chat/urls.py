from django.urls import path
from .views import (
    GroupChatroomList,
    GroupChatroomDetail,
    ChatApiRoot,
    GroupChatList,
    GroupChatDetail,
    RegularChatList,
    RegularChatDetail
)

urlpatterns = [
    path('', ChatApiRoot.as_view(), name='chat-root'),
    path('group_chatrooms/', GroupChatroomList.as_view(), name='group-chatroom-list'),
    path('group_chatrooms/<int:pk>/', GroupChatroomDetail.as_view(), name='group-chatroom-detail'),
    path('group_chats/', GroupChatList.as_view(), name='group-chat-list'),
    path('group_chats/<int:pk>/', GroupChatDetail.as_view(), name='group-chat-detail'),
    path('regular_chats/', RegularChatList.as_view(), name='regular-chat-list'),
    path('regular_chats/<int:pk>/', RegularChatDetail.as_view(), name='regular-chat-detail'),
]

