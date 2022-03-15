from django.urls import path
from .views import GroupList, GroupDetail

urlpatterns = [
    path('', GroupList.as_view(), name="group-list"),
    path('<int:pk>/', GroupDetail.as_view(), name="group-detail"),
]