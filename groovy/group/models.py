from django.db import models
from user.models import User, TimeStampMixin


class Group(TimeStampMixin):

    OPENED = "OPENED"
    CLOSED = "CLOSED"
    FULL = "FULL"

    GROUP_STATUS = (
        (OPENED, "OPENED"),
        (CLOSED, "CLOSED"),
        (FULL, "FULL"),
    )

    id = models.BigAutoField(primary_key=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="managing_groups")
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=1000)
    quota = models.PositiveSmallIntegerField(null=True)
    has_no_quota = models.BooleanField(default=False)
    is_approval_needed = models.BooleanField(default=True)
    status = models.CharField(choices=GROUP_STATUS, default=GROUP_STATUS[0][0], max_length=10)
    status_changed_at = models.DateTimeField(null=True)

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
    requestor = models.ManyToManyField(User, related_name='join_requests')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='join_requests')
    status = models.CharField(choices=REQUEST_STATUS, max_length=15, default=REQUEST_STATUS[2][0])
    status_changed_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'group_join_request'

    def __repr__(self):
        return f"JoinRequest(id={self.id}, user={self.requestor}, to={self.group})"


class GroupMember(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="members")
    member = models.ManyToManyField(User, related_name="members")
    is_manager = models.BooleanField(default=False)

    class Meta:
        db_table = 'group_member'

    def __repr__(self):
        return f"GroupMember(id={self.id}, group={self.group}, member={self.member})"


class GroupBookmark(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    user = models.ManyToManyField(User, related_name="bookmarks")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="bookmarks")

    class Meta:
        db_table = 'group_bookmark'

    def __repr__(self):
        return f"GroupBookmark(id={self.id}, user={self.user}, group={self.group})"




