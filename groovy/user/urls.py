from django.urls import path
from user import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.api_root),
    path('university/', views.UniversityList.as_view(), name='university-list'),
    path('university/<int:pk>', views.UniversityDetail.as_view(), name='university-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
  ]

urlpatterns = format_suffix_patterns(urlpatterns)