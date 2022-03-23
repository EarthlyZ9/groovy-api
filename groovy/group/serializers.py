from rest_framework import serializers
from group.models import Group, GroupJoinRequest, GroupMember
from user.serializers import SimplifiedUserSerializer, UserSerializer


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    manager = SimplifiedUserSerializer(read_only=True)
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='group-member-detail')

    class Meta:
        model = Group
        fields = [
            "id",
            "manager",
            "title",
            "content",
            "quota",
            "has_no_quota",
            "is_approval_needed",
            "members",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "manager",
            "created_at",
            "updated_at",
        ]


class GroupJoinRequestSerializer(serializers.HyperlinkedModelSerializer):
    requestor = SimplifiedUserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)

    class Meta:
        model = GroupJoinRequest
        fields = [
            "url",
            "id",
            "requestor",
            "group",
            "status",
            "status_changed_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "url",
            "id",
            "requestor",
            "group",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            'url': {'view_name': 'join-request-detail'},
        }


class GroupMemberSerializer(serializers.HyperlinkedModelSerializer):
    # group = GroupSerializer(read_only=True)
    member = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = GroupMember
        fields = [
            "url",
            "id",
            "group",
            "member",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "url",
            "id",
            "group",
            "member",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            'url': {'view_name': 'group-member-detail'},
        }
