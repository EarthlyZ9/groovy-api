from datetime import datetime

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response

from chat.services import ChatService
from group.models import Group, GroupJoinRequest, GroupMember, GroupBookmark
from group.permissions import (
    IsManagerOrReadOnly,
    ManagerOnly,
    IsBookmarkOwner,
    IsManagerOrMember,
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

        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsManagerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]

    # Retrieve 할 때 bookmark 되어 있는지, 되어 있다면 그 ID 값을 같이 반환해줌 (북마크 표시 위함)
    def retrieve(self, request, *args, **kwargs):
        group_id = kwargs.get("pk")
        group = Group.objects.filter(id=group_id).first()
        bookmark_id = group.bookmarks.get('id', None)
        return Response(
            {'group-info': GroupSerializer(group).data, 'bookmark': bookmark_id}, status=status.HTTP_201_CREATED
        )


class CreateGroupJoinRequest(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        group_id = kwargs.get("pk")
        group = get_object_or_404(Group, pk=group_id)

        join_request = GroupService.create_join_request(request.user, group)
        ChatService.join_request_chat(request.user, group)
        NotificationService.notify_join_request(request.user, group)

        return Response(
            GroupJoinRequestSerializer(join_request).data, status=status.HTTP_201_CREATED
        )


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

    def put(self, request, *args, **kwargs):
        # 수락 시 requestor 에게 알림 보내고, member 에 추가
        group_id = kwargs.get("pk")
        group = get_object_or_404(Group, pk=group_id)
        requestor = kwargs.get("requestor")

        changed_status = kwargs.get("status")
        if changed_status == GroupJoinRequest.ACCEPTED:
            GroupService.add_group_member(group, requestor)
            NotificationService.notify_join_request_result(
                requestor, group, changed_status
            )

        # 거절 시 requestor 에게 알림 보내기
        elif changed_status == GroupJoinRequest.REFUSED:
            NotificationService.notify_join_request_result(
                requestor, group, changed_status
            )

        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save(status_changed_at=datetime.now())


class GroupMemberList(generics.ListCreateAPIView):
    queryset = GroupMember.objects.all().order_by("member")
    serializer_class = GroupMemberSerializer
    permission_classes = [IsManagerOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get("pk")
        queryset = GroupMember.objects.filter(group_id=group_id).order_by("member")
        return queryset

    def perform_create(self, serializer):
        group_id = self.kwargs.get("pk")
        serializer.save(group_id=group_id)


class GroupMemberDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrMember]

    def get_queryset(self):
        group_id = self.kwargs.get("pk")
        member_id = self.kwargs.get("member_id")
        queryset = GroupMember.objects.filter(id=member_id, group_id=group_id)
        return queryset


class CreateGroupBookmark(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        group_id = kwargs.get("pk")
        bookmark = GroupService.create_bookmark(request.user, group_id)
        return Response(
            GroupBookmarkSerializer(bookmark).data, status=status.HTTP_201_CREATED
        )


class DestroyGroupBookmark(generics.DestroyAPIView):
    permission_classes = [IsBookmarkOwner]

    def destroy(self, request, *args, **kwargs):
        group_id = self.kwargs.get("pk")
        bookmark_id = self.kwargs.get("bookmark_id")
        instance = GroupBookmark.objects.filter(id=bookmark_id, group_id=group_id)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
