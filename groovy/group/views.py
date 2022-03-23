from rest_framework import generics
from django.db.models import Count
from group.models import Group, GroupJoinRequest, GroupMember
from group.serializers import GroupSerializer, GroupJoinRequestSerializer, GroupMemberSerializer
from rest_framework.reverse import reverse
from rest_framework.response import Response


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupJoinRequestList(generics.ListCreateAPIView):
    queryset = GroupJoinRequest.objects.all()
    serializer_class = GroupJoinRequestSerializer


class GroupJoinRequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupJoinRequest.objects.all()
    serializer_class = GroupJoinRequestSerializer


class GroupMemberList(generics.ListCreateAPIView):
    queryset = GroupMember.objects.all().order_by('group__id')
    # queryset = GroupMember.objects.values('group__id').annotate(members=Count('group__id')).order_by('-created_at')
    serializer_class = GroupMemberSerializer


class GroupMemberDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GroupMember.objects.all()
    serializer_class = GroupMemberSerializer


class GroupApiRoot(generics.GenericAPIView):
    name = 'Group'

    def get(self, request, *args, **kwargs):
        return Response({
            'groups': reverse('group-list', request=request),
            'group_members': reverse('group-member-list', request=request),
            'group_join_request': reverse('join-request-list', request=request),
            })
