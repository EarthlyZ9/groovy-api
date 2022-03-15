from django.db import models
from user.models import User, TimeStampMixin


class Group(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="managing_groups")
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=1000)
    quota = models.PositiveSmallIntegerField(null=True)
    has_no_quota = models.BooleanField(default=False)
    is_approval_needed = models.BooleanField(default=True)

    class Meta:
        db_table = 'group'

    def __repr__(self):
        return f"Group({self.id}, {self.title})"


class GroupJoinRequest(TimeStampMixin):

    REFUSED = "REFUSED"
    ACCEPTED = "ACCEPTED"
    PENDING = "PENDING"
    REQUEST_STATUS = (
        (REFUSED, "REFUSED"),
        (ACCEPTED, "ACCEPTED"),
        (PENDING, "PENDING"),
    )

    id = models.BigAutoField(primary_key=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.CharField(choices=REQUEST_STATUS, max_length=15)
    status_changed_at = models.DateTimeField()

    class Meta:
        db_table = 'group_join_request'

    def __repr__(self):
        return f"JoinRequest(id={self.id}, user={self.user_id}, to={self.group_id})"


class GroupMember(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'group_member'

    def __repr__(self):
        return f"GroupMember(id={self.id}, group={self.group_id}, member={self.user_id})"






