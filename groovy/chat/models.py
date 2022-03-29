from django.db import models
from user.models import User, TimeStampMixin
from group.models import Group


class GroupChatroom(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'group_chatroom'

    def __repr__(self):
        return f"GroupChatroom({self.id}, {self.group_id})"


class GroupChat(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    chatroom = models.ForeignKey(GroupChatroom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)

    class Meta:
        db_table = 'group_chat'

    def __repr__(self):
        return f"GroupChat(id={self.id}, chatroom={self.chatroom}, user={self.user})"


class RegularChat(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="regular_chat_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="regular_chat_receiver")
    content = models.CharField(max_length=1000)

    class Meta:
        db_table = 'regular_chat'

    def __repr__(self):
        return f"RegularChat(id={self.id}, sender={self.sender}, receiver={self.receiver})"








