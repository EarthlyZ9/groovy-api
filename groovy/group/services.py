from datetime import datetime

from group.models import GroupJoinRequest, GroupMember, GroupBookmark


class GroupService:
    @staticmethod
    def create_join_request(requestor, group):
        return GroupJoinRequest.objects.create(requestor=requestor, group=group)

    @staticmethod
    def add_group_member(group, member):
        return GroupMember.objects.create(group=group, member=member)

    @staticmethod
    def delete_group_member(group, member):
        obj = GroupMember.objects.filter(group=group, member=member).first()
        obj.delete()
        if obj.DoesNotExist:
            return True

    @staticmethod
    def create_bookmark(user, group_id):
        return GroupBookmark.objects.create(user=user, group_id=group_id)

    @staticmethod
    def get_bookmark(user, group):
        bookmark = GroupBookmark.objects.filter(user=user, group=group).first()
        if bookmark.exist():
            return bookmark
        else:
            return None

    @staticmethod
    def update_join_request_status(obj, changed_status):
        obj.status = changed_status
        obj.status_changed_at = datetime.now()
        return obj
