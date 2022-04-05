from django.db import transaction

from group.models import GroupJoinRequest, GroupMember, GroupBookmark


class GroupService:
    @staticmethod
    @transaction.atomic
    def create_join_request(requestor, group):
        return GroupJoinRequest.objects.create(requestor=requestor, group=group)

    @staticmethod
    def add_group_member(group, requestor):
        return GroupMember.objects.create(group=group, member=requestor)

    @staticmethod
    def create_bookmark(user, group_id):
        return GroupBookmark.objects.create(user=user, group_id=group_id)
