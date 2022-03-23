from django.urls import path
from .views import FriendApiRoot, FriendList, FriendDetail, FriendRequestList, FriendRequestDetail

urlpatterns = [
    path('', FriendApiRoot.as_view(), name='friend-root'),
    path('friends/', FriendList.as_view(), name='friend-list'),
    path('friends/<int:pk>/', FriendDetail.as_view(), name='friend-detail'),
    path('friend_requests/', FriendRequestList.as_view(), name='friend-request-list'),
    path('friend_requests/<int:pk>/', FriendRequestDetail.as_view(), name='friend-request-detail'),
]
