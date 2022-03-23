from django.urls import path
from .views import (
    GroupList,
    GroupDetail,
    GroupApiRoot,
    GroupJoinRequestList,
    GroupJoinRequestDetail,
    GroupMemberList,
    GroupMemberDetail
)

urlpatterns = [
    path('', GroupApiRoot.as_view(), name="group-root"),
    path('groups/', GroupList.as_view(), name="group-list"),
    path('groups/<int:pk>/', GroupDetail.as_view(), name="group-detail"),
    path('group-members/', GroupMemberList.as_view(), name="group-member-list"),
    path('group-members/<int:pk>', GroupMemberDetail.as_view(), name="group-member-detail"),
    path('join-requests/', GroupJoinRequestList.as_view(), name="join-request-list"),
    path('join-requests/<int:pk>/', GroupJoinRequestDetail.as_view(), name="join-request-detail"),
]