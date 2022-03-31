from django.db import transaction

from group.models import GroupJoinRequest


class GroupService:
    @staticmethod
    @transaction.atomic
    def create_join_request(requestor, group):
        return GroupJoinRequest.objects.create(requestor=requestor, group=group)


