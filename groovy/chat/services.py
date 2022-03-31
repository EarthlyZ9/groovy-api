from chat.models import RegularChat

class ChatService:
    @staticmethod
    def notify_join_request(requestor, group):
        content = f"'{group.title}' 그룹에 쪼인하고 싶어요!"
        return RegularChat.objects.create(sender=requestor, receiver_id=group.manager_id, content=content,
                                   is_join_request_message=True)