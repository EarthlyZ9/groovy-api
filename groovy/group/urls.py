from django.urls import path

from .views import (
    GroupList,
    GroupDetail,
    GroupJoinRequestList,
    GroupJoinRequestDetail,
    GroupBookmarkList,
    GroupBookmarkDetail,
)

urlpatterns = [
    path("", GroupList.as_view(), name="group-list"),
    path("<int:pk>/", GroupDetail.as_view(), name="group-detail"),
    path(
        "<int:pk>/join-requests/",
        GroupJoinRequestList.as_view(),
        name="join-request-list",
    ),
    path(
        "join-requests/<int:pk>/",
        GroupJoinRequestDetail.as_view(),
        name="join-request-detail",
    ),
    path(
        "<int:pk>/bookmarks/",
        GroupBookmarkList.as_view(),
        name="group-bookmark-list",
    ),
    path(
        "bookmarks/<int:pk>/",
        GroupBookmarkDetail.as_view(),
        name="group-bookmark-detail",
    ),
]
