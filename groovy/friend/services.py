from friend.models import FriendRequest
from friend.serializers import FriendRequestSerializer


class FriendService:

    @staticmethod
    def send_friend_request(request_from, request_to):
        friend_request, created = FriendRequest.objects.get_or_create(request_from=request_from, request_to=request_to)
        return friend_request, created

    @staticmethod
    def get_latest_friend_request(user):
        latest_request = FriendRequest.objects.filter(request_to=user).order_by('created_at').first()
        serializer = FriendRequestSerializer(latest_request)
        return serializer.data

    @staticmethod
    def change_friend_request_status():
        # 수락 or 거절, 수락 시 friend model 에 추가 + 알림 보내기
        pass

    @staticmethod
    def count_friend_request(user):
        return FriendRequest.objects.filter(request_to=user).count()

    @staticmethod
    def cancel_friend_request():
        pass

    @staticmethod
    def is_friend():
        pass
