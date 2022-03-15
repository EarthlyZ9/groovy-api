import logging
from datetime import datetime
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    use_in_migrations = True

    def create_user(
        self,
        email=None,
        password=None,
        **extra_fields,
    ):
        """
        Create and save a User with the given email and password.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if not email:
            raise ValueError("Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        logging.info(f"User [{user.id}] 회원가입")
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, password=password, **extra_fields)


class TimeStampMixin(models.Model):
    """
    abstract timestamp mixin base model for created_at, updated_at field
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, TimeStampMixin):

    MALE = "MALE"
    FEMALE = "FEMALE"
    GENDER_CHOICES = (
        (None, "NONE"),
        (MALE, "MALE"),
        (FEMALE, "FEMALE"),
    )

    ADMISSION_YEAR = [(r,r) for r in range(2000, datetime.now().year+2)]

    FRESHMEN = 1
    SOPHOMORE = 2
    JUNIOR = 3
    SENIOR = 4
    GRADE_CHOICES = (
        (FRESHMEN, 1),
        (SOPHOMORE, 2),
        (JUNIOR, 3),
        (SENIOR, 4),
    )

    OTHER = '기타'
    DELETE_REASONS = (
        (OTHER, _('기타')),
    )

    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=64, unique=True, null=True)
    name = models.CharField(max_length=20, default="", help_text="실명")
    nickname = models.CharField(max_length=20, blank=True, default="", help_text="서비스 상에서 사용되는 이름")
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES)
    birth_date = models.DateTimeField()

    university = models.ForeignKey('University', on_delete=models.DO_NOTHING)
    is_university_confirmed = models.BooleanField(default=False)
    university_confirmed_at = models.DateTimeField()

    admission_class = models.SmallIntegerField(choices=ADMISSION_YEAR, default=datetime.now().year)
    grade = models.SmallIntegerField(choices=GRADE_CHOICES)

    profile_image_url = models.URLField(max_length=256, blank=True, default="")
    thumbnail_image_url = models.URLField(max_length=256, blank=True, default="")

    is_service_terms_agreed = models.BooleanField(default=False)
    is_push_allowed = models.BooleanField(default=False)
    push_id = models.CharField(null=True, max_length=64)

    login_attempt_at = models.DateTimeField(null=True)
    last_login_at = models.DateTimeField(null=True)

    app_version = models.CharField(null=True, max_length=16)
    auth_token = models.CharField(null=True, max_length=128)

    is_deleted = models.BooleanField(default=False)
    deleted_reason = models.CharField(choices=DELETE_REASONS, max_length=255, blank=True, null=True)
    deleted_at = models.DateTimeField()

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    class Meta:
        db_table = "user"
        unique_together = ["email"]
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"[{self.id}] {self.get_username()}"

    def __repr__(self):
        return f"User({self.id}, {self.get_username()})"

    def get_username(self):
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class UserSuggestion(TimeStampMixin):

    OTHER = '기타'
    SUGGESTION_TYPES = (
        (OTHER, _('기타'))
    )

    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    suggestion_type = models.CharField(max_length=16)
    content = models.TextField()

    class Meta:
        db_table = 'user_suggestion'


class University(TimeStampMixin):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'university'
