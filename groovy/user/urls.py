from django.urls import path
from user import views

urlpatterns = [
    path("", views.UserApiRoot.as_view(), name='user-root'),
    path('universities/', views.UniversityList.as_view(), name='university-list'),
    path('universities/<int:pk>/', views.UniversityDetail.as_view(), name='university-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
  ]
