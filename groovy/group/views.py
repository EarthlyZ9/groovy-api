from rest_framework import generics, permissions
from group.permissions import IsManagerOrReadOnly
from group.models import Group, GroupJoinRequest, GroupMember, GroupBookmark
from group.serializers import (
    GroupSerializer,
    GroupJoinRequestSerializer,
    GroupMemberSerializer,
    GroupBookmarkSerializer)
from rest_framework.reverse import reverse
from rest_framework.response import Response

# TODO: GroupDetail bookmark
# TODO: GroupList filter
# TODO: GroupList search
# TODO: GroupList order


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)  # when created, add request.user as manager


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsManagerOrReadOnly, permissions.IsAuthenticatedOrReadOnly]


class GroupJoinRequestList(generics.ListCreateAPIView):
    queryset = GroupJoinRequest.objects.all()
    serializer_class = GroupJoinRequestSerializer


class GroupJoinRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupJoinRequest.objects.all()
    serializer_class = GroupJoinRequestSerializer


class GroupMemberList(generics.ListCreateAPIView):
    queryset = GroupMember.objects.all().order_by('group__id')
    serializer_class = GroupMemberSerializer


class GroupMemberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer


class GroupBookmarkList(generics.ListCreateAPIView):
    queryset = GroupBookmark.objects.all()
    serializer_class = GroupBookmarkSerializer


class GroupBookmarkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupBookmark.objects.all()
    serializer_class = GroupBookmarkSerializer


class GroupApiRoot(generics.GenericAPIView):
    name = 'Group'

    def get(self, request, *args, **kwargs):
        return Response({
            'groups': reverse('group-list', request=request),
            'group_members': reverse('group-member-list', request=request),
            'group_join_requests': reverse('join-request-list', request=request),
            'group_bookmarks': reverse('group-bookmark-list', request=request),
            })
