from rest_framework import serializers
from group.models import Group, GroupJoinRequest, GroupMember, GroupBookmark
from user.serializers import SimplifiedUserSerializer


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    manager = SimplifiedUserSerializer(read_only=True)
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='group-member-detail')
    bookmark_count = serializers.IntegerField(source='bookmarks.count', read_only=True)

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
            "bookmark_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "manager",
            "bookmark_count",
            "created_at",
            "updated_at",
        ]


class MiniGroupSerializer(serializers.HyperlinkedModelSerializer):
    manager = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = Group
        fields = [
            "id",
            "title",
            "manager",
            "quota",
            "has_no_quota",
            "is_approval_needed",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "title",
            "manager",
            "quota",
            "has_no_quota",
            "is_approval_needed",
            "created_at",
            "updated_at",
        ]


class GroupJoinRequestSerializer(serializers.HyperlinkedModelSerializer):
    requestor = SimplifiedUserSerializer(read_only=True)
    group = MiniGroupSerializer(read_only=True)

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
    group = MiniGroupSerializer(read_only=True)
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


class GroupBookmarkSerializer(serializers.HyperlinkedModelSerializer):
    group = MiniGroupSerializer(read_only=True)
    user = SimplifiedUserSerializer(read_only=True)

    class Meta:
        model = GroupBookmark
        fields = [
            "url",
            "id",
            "group",
            "user",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "url",
            "id",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            'url': {'view_name': 'group-bookmark-detail'},
        }
