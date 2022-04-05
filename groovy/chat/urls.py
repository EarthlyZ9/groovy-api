from django.urls import path
from .views import (
    ChatList,
    GroupChatDetail,
    PersonalChatDetail,
)

urlpatterns = [
    path("", ChatList.as_view(), name="chat-list"),
    path("group_chatroom/<int:pk>/", GroupChatDetail.as_view(), name="group-chat"),
    path(
        "personal_chatroom/<int:pk>/",
        PersonalChatDetail.as_view(),
        name="personal-chat",
    ),
]
