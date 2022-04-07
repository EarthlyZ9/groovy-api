from django.urls import path

from .views import (
    FriendList,
    FriendDetail,
    FriendRequestList,
    FriendRequestDetail,
    UserSearch,
    SendFriendRequest,
)

urlpatterns = [
    path("", FriendList.as_view(), name="friend-list"),
    path("<int:pk>/", FriendDetail.as_view(), name="friend-detail"),  # 친구 프로필
    path("friend_requests/", FriendRequestList.as_view(), name="friend-request-list"),
    path("friend-requests/<int:pk>", FriendRequestDetail.as_view(), name="friend-request-detail"),
    path("search-user/", UserSearch.as_view(), name="search-user"),
    path("search-user/<int:pk>/", SendFriendRequest.as_view(), name="send-friend-request"),

]
