import logging
from django.db import models
from user.models import User, TimeStampMixin


class Friend(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_id")
    friend_id = models.ManyToManyField(User, related_name="friend_id")

    def __repr__(self):
        return f"Friend(id={self.id}, user={self.user_id}, friend={self.friend_id})"


class FriendRequest(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    request_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_from")
    request_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_to")
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField()

    def __repr__(self):
        return f"FriendRequest(id={self.id}, from={self.request_from}, to={self.request_to})"








