from django.urls import path

from friend.views import SendFriendRequest
from user import views
from user.views import UniversityVerification

urlpatterns = [
    path("universities/", views.UniversityList.as_view(), name="university-list"),
    path(
        "universities/<int:pk>/",
        views.UniversityDetail.as_view(),
        name="university-detail",
    ),
    path("", views.UserList.as_view(), name="user-list"),
    path("<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("<int:pk>/friend-request", SendFriendRequest.as_view(), name="send-friend-request"),
    path("<int:pk>/verify-univ", UniversityVerification.as_view(), name="verify-univ"),
]
