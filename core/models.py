# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# from simple_history.models import HistoricalRecords


class CoreUserManager(UserManager):
    """ changed to use email is main id field """

    #  def _create_user(self, username, email, password, **extra_fields):
    def username_from_email(self, email, obfuscate_with="*"):
        return email  # TODO implement obfuscation x

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if not username:
            username = self.username_from_email(email)

        return self._create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        if not username:
            username = self.username_from_email(email)

        return self._create_user(username=username, email=email, password=password, **extra_fields)


class CoreUser(AbstractBaseUser, PermissionsMixin):
    """
    implements basic auth
    """
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "core_user"

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=100,
        help_text=_(
            "Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        blank=True,
        default="",
    )

    email = models.EmailField(_("email address"), blank=False, unique=True)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def admin_display_name(self):
        if self.username:
            return f"{self.username} ({self.email})"
        else:
            return self.email


class Profile(models.Model):
    """ implements simple data about person
    """
    _name_length = 512

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT)

    first_name = models.CharField(_("first name"), max_length=_name_length, db_index=True)
    last_name = models.CharField(_("last name"), max_length=_name_length, db_index=True)
    middle_name = models.CharField(_("middle name"), max_length=_name_length, blank=True)

    date_of_birth = models.DateField(blank=True, null=True)

    # history = HistoricalRecords()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def __str__(self):
        full_name = self.get_full_name()
        if self.owner:
            return f"{full_name} ({self.owner.email})"
        else:
            return full_name
