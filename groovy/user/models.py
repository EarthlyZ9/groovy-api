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
        logging.info(
            f"User [{user.id}] 회원가입"
        )
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

    NONE = "X"
    MALE = "M"
    FEMALE = "F"
    GENDER_CHOICES = (
        (NONE, "None"),
        (MALE, "MALE"),
        (FEMALE, "FEMALE"),
    )

    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(
        max_length=64, unique=True, null=True, help_text="used as username"
    )

    name = models.CharField(max_length=20, blank=True, default="", help_text="실명")
    nickname = models.CharField(
        max_length=20, blank=True, default="", help_text="서비스 상에서 사용되는 이름"
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=NONE)
    age_range = models.CharField(max_length=8, blank=True, default="")
    phone_number = models.CharField(
        max_length=20, blank=True, default="", help_text="+82 10-XXXX-XXXX"
    )
    profile_image_url = models.URLField(max_length=256, blank=True, default="")
    thumbnail_image_url = models.URLField(max_length=256, blank=True, default="")

    is_service_terms_agreed = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
    )
    date_joined = models.DateTimeField(_("date joined"), default=datetime.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    class Meta:
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
