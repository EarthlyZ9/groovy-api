import logging
from datetime import datetime
from django.db import models
from user.models import User, TimeStampMixin
from django.utils.translation import gettext_lazy as _


class Group(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    manager_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    quota = models.SmallIntegerField(null=True)
    is_no_quota = models.BooleanField(default=False)
    is_approval_process = models.BooleanField(default=True)

    def __repr__(self):
        return f"Group({self.id}, {self.title})"


class JoinRequest(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField()

    def __repr__(self):
        return f"JoinRequest(id={self.group_id}, user={self.user_id}, to={self.group_id})"


class GroupMember(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __repr__(self):
        return f"GroupMember(id={self.group_id}, group={self.group_id}, member={self.user_id})"






