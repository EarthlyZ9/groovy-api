from datetime import datetime

from friend.models import FriendRequest, Friend


class FriendService:

    @staticmethod
    def get_all_friends(queryset, user):
        return queryset.filter(friend_user=user).all().order_by('nickname')

    @staticmethod
    def send_friend_request(request_from, request_to):
        friend_request, created = FriendRequest.objects.get_or_create(request_from=request_from, request_to=request_to)
        return friend_request, created

    @staticmethod
    def get_all_friend_request(user):
        return FriendRequest.objects.filter(request_to=user).all().order_by('created_at')

    @staticmethod
    def update_friend_request_status(obj, changed_status):
        obj.status = changed_status
        obj.status_changed_at = datetime.now()
        return obj

    @staticmethod
    def add_friend(request_from, request_to):
        Friend.objects.create(user=request_from, friend=request_to)
        Friend.objects.create(user=request_to, friend=request_from)
        return None

    @staticmethod
    def delete_friend(obj):
        user = obj.user
        friend = obj.friend
        obj.delete()
        Friend.objects.filter(user=friend, friend=user).first().delete()
