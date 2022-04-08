from django.urls import path

from .views import (
    FriendList,
    FriendDetail,
    FriendRequestList,
    UpdateFriendRequest,
)

urlpatterns = [
    path("", FriendList.as_view(), name="friend-list"),
    path("<int:pk>/", FriendDetail.as_view(), name="friend-detail"),
    path("friend-requests/", FriendRequestList.as_view(), name="friend-request-list"),
    path("friend-requests/<int:pk>", UpdateFriendRequest.as_view(), name="friend-request-detail"),
]
