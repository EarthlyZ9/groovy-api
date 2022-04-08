from group.models import GroupJoinRequest
from user.models import UserNotification


class NotificationService:
    @staticmethod
    def notify_join_request(requestor, group):
        notification_type = UserNotification.JOIN_REQUEST_RECEIVED
        content = f"{requestor}님이 '{group.title}' 그룹에 쪼인 요청을 보냈어요!"
        return UserNotification.objects.create(
            user_id=group.manager_id,
            notificaton_type=notification_type,
            content=content,
            redirect_url="chat/",
        )

    @staticmethod
    def notify_join_request_result(requestor, group, status):
        if status == GroupJoinRequest.ACCEPTED:
            notification_type = UserNotification.JOIN_REQUEST_ACCEPTED
            content = f"신청했던 '{group.title}' 그룹에 쪼인되었어요!"
            return UserNotification.objects.create(
                user=requestor,
                notificaton_type=notification_type,
                content=content,
                redirect_url="chat/",
            )
        elif status == GroupJoinRequest.REFUSED:
            notification_type = UserNotification.JOIN_REQUEST_ACCEPTED
            content = f"요청했던 '{group.title}' 그룹에 쪼인이 거절되었어요. T_T"
            return UserNotification.objects.create(
                user=requestor,
                notificaton_type=notification_type,
                content=content,
                redirect_url=f"group/{group.id}/",
            )

    @staticmethod
    def notify_friend_request(request_from, request_to):
        notification_type = UserNotification.FRIEND_REQUEST_RECEIVED
        content = f"'{request_from}'(이)가 친구 요청을 했어요!"
        return UserNotification.objects.create(
            user=request_to,
            notificaton_type=notification_type,
            content=content,
            redirect_url="chat/",
        )

    @staticmethod
    def notify_friend_request_accepted(request_from, request_to):
        notification_type = UserNotification.FRIEND_REQUEST_ACCEPTED
        content = f"'{request_from}'(와)과 친구가 되었어요!"
        return UserNotification.objects.create(
            user=request_to,
            notification_type=notification_type,
            cotent=content,
            redirect_url="friend/",
        )
