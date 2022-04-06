from django.urls import path
from .views import (
    ChatRoomList,
    GroupChatDetail,
    PersonalChatDetail,
)

urlpatterns = [
    path("", ChatRoomList.as_view(), name="chat-list"),
    path("group-chatroom/<int:pk>/", GroupChatDetail.as_view(), name="group-chat"),
    path(
        "personal-chatroom/<int:pk>/",
        PersonalChatDetail.as_view(),
        name="personal-chat",
    ),
]
