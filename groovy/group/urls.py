from django.urls import path
from .views import (
    GroupList,
    GroupDetail,
    GroupApiRoot,
    CreateGroupJoinRequest,
    GroupJoinRequestDetail,
    GroupMemberList,
    GroupMemberDetail, GroupBookmarkList, GroupBookmarkDetail,
)

urlpatterns = [
    # path('', GroupApiRoot.as_view(), name="group-root"),
    path('', GroupList.as_view(), name="group-list"),
    path('<int:pk>/', GroupDetail.as_view(), name="group-detail"),
    path('<int:pk>/group-members/', GroupMemberList.as_view(), name="group-member-list"),
    path('<int:pk>/group-members/<int:member_id>', GroupMemberDetail.as_view(), name="group-member-detail"),
    path('<int:pk>/join-requests/', CreateGroupJoinRequestls.as_view(), name="join-request-list"),
    path('<int:pk>/join-requests/<int:request_id>/', GroupJoinRequestDetail.as_view(), name="join-request-detail"),
    path('<int:pk>/bookmarks/', GroupBookmarkList.as_view(), name='group-bookmark-list'),
    path('<int:pk>/bookmarks/<int:bookmark_id>/', GroupBookmarkDetail.as_view(), name='group-bookmark-detail'),
]
