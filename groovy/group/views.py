from datetime import datetime

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters, status

from chat.services import ChatService
from config.Response import Response
from group.models import Group, GroupJoinRequest, GroupBookmark
from group.permissions import (
    ManagerOnly,
    IsBookmarkOwner,
)
from group.serializers import (
    GroupSerializer,
    GroupJoinRequestSerializer,
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
    # permission_classes = [IsManagerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [permissions.AllowAny]

    # def retrieve(self, request, *args, **kwargs):
    #     group = self.get_object()
    #     bookmark = GroupService.get_bookmark(request.user, group)
    #     return Response(data={'group_data': GroupSerializer(group).data, 'bookmark': bookmark})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        group = self.get_object()
        data = request.data

        # TODO: manually adding members to group
        additional_members = request.data.get("member")
        if additional_members:
            if group.member is None:
                ChatService.create_group_chatroom(group=group)
            GroupService.add_group_member(group, additional_members)
            del data['member']  # member data 초기화

        serializer = self.get_serializer(group, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            updated_at=datetime.now()
        )

        return Response(data=serializer.data)


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


class GroupJoinRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupJoinRequestSerializer
    permission_classes = [ManagerOnly]
    queryset = GroupJoinRequest.objects.all()

    def patch(self, request, *args, **kwargs):
        join_request_obj = self.get_object()
        group = join_request_obj.group
        requestor = join_request_obj.requestor
        changed_status = request.data.get("status")

        updated_join_request_obj = GroupService.update_join_request_status(join_request_obj, changed_status)

        if changed_status == GroupJoinRequest.ACCEPTED:
            if group.members is None:
                ChatService.create_group_chatroom(group)
            GroupService.add_group_member(group, requestor.id)

        NotificationService.notify_join_request_result(
            requestor, group, changed_status
        )

        return Response(data=GroupJoinRequestSerializer(updated_join_request_obj).data)


# class GroupMemberList(generics.ListCreateAPIView):
#     queryset = GroupMember.objects.all()
#     serializer_class = GroupMemberSerializer
#     #permission_classes = [IsManagerOrReadOnly, permissions.IsAuthenticated]
#     permission_classes = [permissions.AllowAny]
#
#     def get_queryset(self):
#         group_id = self.kwargs.get("pk")
#         queryset = GroupMember.objects.filter(group_id=group_id).order_by("member")
#         return queryset
#
#     def create(self, request, *args, **kwargs):
#         group_id = kwargs.get("pk")
#         group = get_object_or_404(Group, pk=group_id)
#
#         if GroupMember.objects.filter(group=group) is None:
#             ChatService.create_group_chatroom(group=group)
#
#         new_member = request.data["userId"]
#         print(new_member)
#         group_member = GroupService.add_group_member(group, new_member)
#         return Response(data=GroupMemberSerializer(group_member).data)


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
