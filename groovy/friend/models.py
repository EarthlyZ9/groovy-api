from django.db import models
from user.models import User, TimeStampMixin


class Friend(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_user")
    friend_id = models.ManyToManyField(User, related_name="friends")

    class Meta:
        db_table = 'friend'

    def __repr__(self):
        return f"Friend(id={self.id}, user={self.user_id}, friend={self.friend_id})"


class FriendRequest(TimeStampMixin):

    REFUSED = "REFUSED"
    ACCEPTED = "ACCEPTED"
    PENDING = "PENDING"
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

    class Meta:
        db_table = 'friend_request'

    def __repr__(self):
        return f"FriendRequest(id={self.id}, from={self.request_from_id}, to={self.request_to_id})"








