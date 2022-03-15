import logging
from django.db import models
from groovy.user.models import User, TimeStampMixin


class Friend(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_user")
    friend_id = models.ManyToManyField(User, related_name="friends")

    def __repr__(self):
        return f"Friend(id={self.id}, user={self.user}, friend={self.friend_id})"


class FriendRequest(TimeStampMixin):

    REFUSED = "R"
    ACCEPTED = "A"
    PENDING = "P"
    REQUEST_STATUS = (
        (REFUSED, "REFUSED"),
        (ACCEPTED, "ACCEPTED"),
        (PENDING, "PENDING"),
    )

    id = models.BigAutoField(primary_key=True)
    request_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_from")
    request_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="request_to")
    status = models.CharField(choices=REQUEST_STATUS, max_length=15)
    status_changed_at = models.DateTimeField()

    def __repr__(self):
        return f"FriendRequest(id={self.id}, from={self.request_from}, to={self.request_to})"








