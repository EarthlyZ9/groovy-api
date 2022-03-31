from user.models import UserNotification


class NotificationService:
    @staticmethod
    def notify_join_request(requestor, group):
        notification_type = UserNotification.JOIN_REQUEST_RECEIVED
        content = f"{requestor}님이 '{group.title}' 그룹에 쪼인 요청을 보냈어요!"
        return UserNotification.objects.create(user_id=group.manager_id, notificaton_type=notification_type,
                                               content=content, redirect_url='chat/')

    @staticmethod
    def notify_join_request_result():
        pass