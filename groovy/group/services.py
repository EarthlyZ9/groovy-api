from datetime import datetime

from group.models import GroupJoinRequest, GroupBookmark, Group
from user.models import User


class GroupService:
    @staticmethod
    def create_join_request(requestor, group):
        return GroupJoinRequest.objects.create(requestor=requestor, group=group)

    @staticmethod
    def add_group_member(group, additional_members):
        if type(additional_members) == list:
            # TODO: iterate through additional members and adding to group - member field
            for user_id in additional_members:
                user = User.objects.get(id=user_id)
                group.member.add(user)
        else:
            # request 수락 시 단일 객체
            user = User.objects.get(id=additional_members)
            group.member.add(user)
        return Group.objects.get(id=group.id)

    @staticmethod
    def delete_group_member(group, member):
        pass

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
