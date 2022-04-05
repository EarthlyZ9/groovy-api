from django.urls import path
from user import views

urlpatterns = [
    path("universities/", views.UniversityList.as_view(), name="university-list"),
    path(
        "universities/<int:pk>/",
        views.UniversityDetail.as_view(),
        name="university-detail",
    ),
    path("", views.UserList.as_view(), name="user-list"),
    path("<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
]
