from rest_framework import generics, permissions, filters, status
from django.http import Http404
from datetime import datetime
from django.db import IntegrityError, transaction
from chat.models import RegularChat
from group.permissions import IsManagerOrReadOnly, ManagerOnly, IsBookmarkOwner, IsManagerOrMember
from group.models import Group, GroupJoinRequest, GroupMember, GroupBookmark
from group.serializers import (
    GroupSerializer,
    GroupJoinRequestSerializer,
    GroupMemberSerializer,
    GroupBookmarkSerializer)
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all().order_by('created_at')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'content', 'manager']

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)  # when created, add request.user as manager

    def get_queryset(self):
        queryset = Group.objects
        user = self.request.user
        queryset = queryset.filter(manager=user)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsManagerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]


class CreateGroupJoinRequest(generics.CreateAPIView):

    serializer_class = GroupJoinRequestSerializer

    def create(self, request, *args, **kwargs):
        group = Group.objects.filter(id=self.kwargs.get('pk')).first()
        user = self.request.user

        if group:
            manager = group.manager
            content = f"'{group.title}' 그룹에 쪼인하고 싶어요!"
            RegularChat.objects.create(sender=user, receiver=manager, content=content, is_join_request_message=True)

        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        group_id = self.kwargs.get("pk")
        serializer.save(requestor=self.request.user, group_id=group_id)


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

"""
class GroupApiRoot(generics.GenericAPIView):
    name = 'Group'

    def get(self, request, *args, **kwargs):
        return Response({
            'groups': reverse('group-list', request=request),
            'group_members': reverse('group-member-list', request=request),
            'group_join_requests': reverse('join-request-list', request=request),
            'group_bookmarks': reverse('group-bookmark-list', request=request),
            })
"""
