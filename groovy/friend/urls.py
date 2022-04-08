from django.urls import path

from .views import (
    FriendList,
    FriendDetail,
    FriendRequestList,
    FriendRequestDetail,
)

urlpatterns = [
    path("", FriendList.as_view(), name="friend-list"),
    path("<int:pk>/", FriendDetail.as_view(), name="friend-detail"),
    path("friend-requests/", FriendRequestList.as_view(), name="friend-request-list"),
    path("friend-requests/<int:pk>", FriendRequestDetail.as_view(), name="friend-request-detail"),
]
