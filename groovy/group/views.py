from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters, status

from chat.services import ChatService
from config.Response import Response
from group.models import Group, GroupJoinRequest, GroupMember, GroupBookmark
from group.permissions import (
    IsManagerOrReadOnly,
    ManagerOnly,
    IsBookmarkOwner,
)
from group.serializers import (
    GroupSerializer,
    GroupJoinRequestSerializer,
    GroupMemberSerializer,
    GroupBookmarkSerializer,
)
from group.services import GroupService
from user.services import NotificationService


class GroupList(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["status"]
    search_fields = ["title", "content", "manager"]

    def perform_create(self, serializer):
        serializer.save(
            manager=self.request.user
        )  # when created, add request.user as manager

    def get_queryset(self):
        queryset = Group.objects.all().order_by("created_at")
        is_mine = self.request.query_params.get("m", "").strip()

        if is_mine:
            queryset = queryset.filter(manager_id=self.request.user.id)

        return queryset


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsManagerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        group = self.get_object()
        bookmark = GroupService.get_bookmark(request.user, group)
        return Response(data={'group_data': GroupSerializer(group).data, 'bookmark': bookmark})


class GroupJoinRequestList(generics.ListCreateAPIView):
    serializer_class = GroupJoinRequestSerializer

    def get_queryset(self):
        group_id = self.kwargs.get("pk")
        queryset = GroupJoinRequest.objects.filter(group_id=group_id).order_by("created_at")
        return queryset

    def create(self, request, *args, **kwargs):
        group_id = kwargs.get("pk")
        group = get_object_or_404(Group, pk=group_id)

        join_request = GroupService.create_join_request(request.user, group)
        ChatService.join_request_chat(request.user, group)
        NotificationService.notify_join_request(request.user, group)

        return Response(
            data=GroupJoinRequestSerializer(join_request).data, status=status.HTTP_201_CREATED
        )


class UpdateGroupJoinRequest(generics.UpdateAPIView):
    serializer_class = GroupJoinRequestSerializer
    permission_classes = [ManagerOnly]

    def get_queryset(self):
        user = self.request.user
        request_id = self.kwargs.get("request_id")
        queryset = GroupJoinRequest.objects.filter(manager=user, request_id=request_id)
        return queryset

    def update(self, request, *args, **kwargs):
        join_request_obj = self.get_object()
        group = join_request_obj.group
        requestor = join_request_obj.requestor
        changed_status = kwargs.get("status")

        updated_join_request_obj = GroupService.update_join_request_status(join_request_obj, changed_status)

        if changed_status == GroupJoinRequest.ACCEPTED:
            GroupService.add_group_member(group, requestor)

        NotificationService.notify_join_request_result(
            requestor, group, changed_status
        )

        return Response(data=GroupJoinRequestSerializer(updated_join_request_obj).data)


class GroupMemberList(generics.ListCreateAPIView):
    queryset = GroupMember.objects.all().order_by("member")
    serializer_class = GroupMemberSerializer
    permission_classes = [IsManagerOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get("pk")
        queryset = GroupMember.objects.filter(group_id=group_id).order_by("member")
        return queryset

    def create(self, request, *args, **kwargs):
        group_id = kwargs.get("pk")
        group = get_object_or_404(Group, pk=group_id)
        new_member = kwargs.get("member")
        group_member = GroupService.add_group_member(group, new_member)
        return Response(data=GroupMemberSerializer(group_member).data)


class GroupBookmarkList(generics.ListCreateAPIView):
    serializer_class = GroupBookmarkSerializer

    def get_queryset(self):
        group_id = self.kwargs.get("pk")
        queryset = GroupBookmark.objects.filter(group_id=group_id).order_by("created_at")
        return queryset

    def create(self, request, *args, **kwargs):
        group_id = kwargs.get("pk")
        bookmark = GroupService.create_bookmark(request.user, group_id)
        return Response(data=GroupBookmarkSerializer(bookmark).data)


class GroupBookmarkDetail(generics.RetrieveDestroyAPIView):
    queryset = GroupBookmark.objects.all()
    serializer_class = GroupBookmarkSerializer
    permission_classes = [IsBookmarkOwner]
