from django.db.models import Count, Prefetch, Q
from rest_framework import serializers
from group.models import Group, GroupJoinRequest, GroupMember, GroupBookmark
from user.serializers import SimplifiedUserSerializer


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    manager = SimplifiedUserSerializer(read_only=True)
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='group-member-detail')
    members_count = serializers.SerializerMethodField()
    join_requests = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='join-request-detail')
    join_requests_count = serializers.SerializerMethodField()
    bookmarks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='group-bookmark-detail')
    bookmarks_count = serializers.SerializerMethodField()

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
            "members_count",
            "join_requests",
            "join_requests_count",
            "bookmarks",
            "bookmarks_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "manager",
            "members_count",
            "join_requests_count",
            "join_requests",
            "bookmarks",
            "bookmarks_count",
            "created_at",
            "updated_at",
        ]

        @staticmethod
        def setup_eager_loading(queryset):
            """ Perform necessary eager loading of data. """
            # select_related for "to-one" relationships
            # queryset = queryset.select_related("author", "category")

            # prefetch_related for "to-many" relationships
            queryset = queryset.prefetch_related('join_requests, bookmarks, members')

            # Prefetch for subsets of relationships
            queryset = (
                queryset.annotate(Count("members", distinct=True))
                .annotate(Count("join_requests", distinct=True))
                .annotate(Count("bookmarks", distinct=True))
            )
            return queryset

        def get_members_count(self, obj):
            return obj.members__count if hasattr(obj, "members__count") else 0

        def get_join_requests_count(self, obj):
            return obj.join_requests__count if hasattr(obj, "join_requests__count") else 0

        def get_bookmarks_count(self, obj):
            return obj.bookmarks__count if hasattr(obj, "bookmarks__count") else 0


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
    requestor = SimplifiedUserSerializer(many=True, read_only=True)
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
            "status_changed_at",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            'url': {'view_name': 'join-request-detail'},
        }


class GroupMemberSerializer(serializers.HyperlinkedModelSerializer):
    group = MiniGroupSerializer(read_only=True)
    member = SimplifiedUserSerializer(many=True, read_only=True)

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
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            'url': {'view_name': 'group-member-detail'},
        }


class GroupBookmarkSerializer(serializers.HyperlinkedModelSerializer):
    group = MiniGroupSerializer(read_only=True)
    user = SimplifiedUserSerializer(many=True, read_only=True)

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
