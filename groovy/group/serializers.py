from django.db.models import Count
from rest_framework import serializers
from group.models import Group, GroupJoinRequest, GroupMember, GroupBookmark
from user.serializers import SimplifiedUserSerializer


class GroupSerializer(serializers.ModelSerializer):
    manager = SimplifiedUserSerializer(read_only=True)
    members = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="group-member-detail"
    )
    members_count = serializers.IntegerField(source="members.count", read_only=True)
    bookmarks = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="group-bookmark-detail"
    )
    bookmarks_count = serializers.IntegerField(source="bookmarks.count", read_only=True)

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
            "status",
            "members",
            "members_count",
            "bookmarks",
            "bookmarks_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "manager",
            "members_count",
            "bookmarks",
            "bookmarks_count",
            "created_at",
            "updated_at",
        ]

    @staticmethod
    def setup_eager_loading(queryset):
        """Perform necessary eager loading of data."""
        # select_related for "to-one" relationships
        # queryset = queryset.select_related("author", "category")

        # prefetch_related for "to-many" relationships
        queryset = queryset.prefetch_related("join_requests, bookmarks, members")

        # Prefetch for subsets of relationships
        queryset = queryset.annotate(
            Count("members", distinct=True).annotate(Count("bookmarks", distinct=True))
        )
        return queryset


class MiniGroupSerializer(serializers.ModelSerializer):
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
            "status",
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
            "status",
            "created_at",
            "updated_at",
        ]


class GroupJoinRequestSerializer(serializers.ModelSerializer):
    requestor = SimplifiedUserSerializer(many=True, read_only=True)
    group = MiniGroupSerializer(read_only=True)

    class Meta:
        model = GroupJoinRequest
        fields = [
            "id",
            "requestor",
            "group",
            "status",
            "status_changed_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "requestor",
            "group",
            "status_changed_at",
            "created_at",
            "updated_at",
        ]


class GroupMemberSerializer(serializers.ModelSerializer):
    group = MiniGroupSerializer(read_only=True)
    member = SimplifiedUserSerializer(many=True, read_only=True)

    class Meta:
        model = GroupMember
        fields = [
            "id",
            "group",
            "member",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "group",
            "created_at",
            "updated_at",
        ]


class GroupBookmarkSerializer(serializers.ModelSerializer):
    group = MiniGroupSerializer(read_only=True)
    user = SimplifiedUserSerializer(many=True, read_only=True)

    class Meta:
        model = GroupBookmark
        fields = ["url", "id", "group", "user", "created_at", "updated_at"]
        read_only_fields = ["url", "id", "group", "user", "created_at", "updated_at"]
