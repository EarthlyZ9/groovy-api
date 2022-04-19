from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken

from group.models import GroupJoinRequest
from user.models import UserNotification, UniversityManualVerification


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


class UserService:
    @staticmethod
    def delete_user(user):
        """
        perform soft delete
        """
        pass

    @staticmethod
    def agree_service_term(user, is_service_terms_agreed):
        if is_service_terms_agreed:
            user.is_service_terms_agreed = is_service_terms_agreed

        user.save(update_fields=["is_service_terms_agreed"])
        return user

    @staticmethod
    def reason_for_leave(user, reason):
        user.deleted_reason = reason
        user.save(update_fields=["deleted_reason"])

        return user

    @staticmethod
    def get_university_verification_request(user):
        university_verification_request = UniversityManualVerification.objects.filter(user=user).first()

        return university_verification_request


def _get_refresh_token_for_user(user):
    return RefreshToken.for_user(user)


def get_tokens_for_user(user):
    refresh = _get_refresh_token_for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
