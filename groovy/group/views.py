from datetime import datetime

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response

from chat.services import ChatService
from group.models import Group, GroupJoinRequest, GroupMember, GroupBookmark
from group.permissions import IsManagerOrReadOnly, ManagerOnly, IsBookmarkOwner, IsManagerOrMember
from group.serializers import (
    GroupSerializer,
    GroupJoinRequestSerializer,
    GroupMemberSerializer,
    GroupBookmarkSerializer
)
from group.services import GroupService
from user.services import NotificationService


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all().order_by('created_at')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'content', 'manager']

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)  # when created, add request.user as manager
    """
    def get_queryset(self):
        queryset = Group.objects
        user = self.request.user
        queryset = queryset.filter(manager=user)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
    """


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsManagerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]


class CreateGroupJoinRequest(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')
        group = get_object_or_404(Group, pk=group_id)

        GroupService.create_join_request(request.user, group)
        ChatService.join_request_chat(request.user, group)
        NotificationService.notify_join_request(request.user, group)

        return Response(GroupJoinRequestSerializer(group).data, status=status.HTTP_201_CREATED)


class GroupJoinRequestDetail(generics.RetrieveUpdateAPIView):
    """
    쪼인요청 받은 사람이 수락 or 거절
    쪼인요청 받은 그룹의 방장만이 read and write
    """

    serializer_class = GroupJoinRequestSerializer
    permission_classes = [ManagerOnly]

    def get_queryset(self):
        user = self.request.user
        request_id = self.kwargs.get("request_id")
        queryset = GroupJoinRequest.objects.filter(manager=user, request_id=request_id)
        return queryset

    # TODO: Override update method to send notification when accepted/refused
    """
    def update(self, request, *args, **kwargs):
        group_id = kwargs.get('pk')
        group = get_object_or_404(Group, pk=group_id)
        status = kwargs.pop('status', False)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    """

    def perform_update(self, serializer):
        serializer.save(status_changed_at=datetime.now())


class GroupMemberList(generics.ListCreateAPIView):
    queryset = GroupMember.objects.all().order_by('member')
    serializer_class = GroupMemberSerializer
    permission_classes = [IsManagerOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get("pk")
        queryset = GroupMember.objects.filter(group_id=group_id).order_by('member')
        return queryset

    def perform_create(self, serializer):
        group_id = self.kwargs.get("pk")
        serializer.save(group_id=group_id)


class GroupMemberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrMember]

    def get_queryset(self):
        group_id = self.kwargs.get('pk')
        member_id = self.kwargs.get("member_id")
        queryset = GroupMember.objects.filter(id=member_id, group_id=group_id)
        return queryset

    def perform_update(self, serializer):
        serializer.save(status_changed_at=datetime.now())


class GroupBookmarkList(generics.ListCreateAPIView):
    queryset = GroupBookmark.objects.all()
    serializer_class = GroupBookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get("pk")
        queryset = GroupMember.objects.filter(group_id=group_id).order_by('member')
        return queryset

    def perform_create(self, serializer):
        group_id = self.kwargs.get("pk")
        serializer.save(user=self.request.user, group_id=group_id)


class GroupBookmarkDetail(generics.RetrieveDestroyAPIView):
    queryset = GroupBookmark.objects.all()
    serializer_class = GroupBookmarkSerializer
    permission_classes = [IsBookmarkOwner]

    def get_queryset(self):
        group_id = self.kwargs.get("pk")
        bookmark_id = self.kwargs.get("bookmark_id")
        queryset = GroupBookmark.objects.filter(id=bookmark_id, group_id=group_id)
        return queryset

