from rest_framework import serializers

from group.models import Group
from user.serializers import ManagerSerializer


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    manager = ManagerSerializer(read_only=True)

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
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "manager",
            "created_at",
            "updated_at",
        ]
