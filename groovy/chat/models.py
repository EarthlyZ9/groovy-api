import logging
from django.db import models
from groovy.user.models import User, TimeStampMixin
from groovy.group.models import Group


class GroupChatroom(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __repr__(self):
        return f"GroupChatroom({self.id}, {self.group_id})"


class GroupChat(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    chatroom_id = models.ForeignKey(GroupChatroom, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)

    def __repr__(self):
        return f"GroupChat(id={self.id}, chatroom={self.chatroom_id}, user={self.user_id})"


class RegularChat(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="regular_chat_sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="regular_chat_receiver")
    content = models.CharField(max_length=1000)

    def __repr__(self):
        return f"RegularChat(id={self.id}, sender={self.sender}, receiver={self.receiver})"








