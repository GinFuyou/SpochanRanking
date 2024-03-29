# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.template import Context, Template
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.personal_chancode import ChanCode


class CoreUserManager(UserManager):
    """ changed to use email is main id field """

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

    objects = CoreUserManager()

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


class CountryChoicesISO(models.IntegerChoices):
    """ using ISO 3166-1 numeric for internal code
        and Alpha-3 for var name
    """
    RUS = 643, _("Russian Federation")


class SportClub(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    country = models.PositiveSmallIntegerField(choices=CountryChoicesISO.choices, default=CountryChoicesISO.RUS)
    locality = models.CharField(max_length=1024, blank=True, default='')
    locality.help_text = _("City or settlement")
    location = models.TextField(max_length=1024, blank=True, default='')

    def __str__(self):
        if self.locality:
            return f"{self.name} ({self.locality})"
        else:
            return self.name


class Profile(models.Model):
    """ implements simple data about person
    """
    _name_length = 512

    owner = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT)

    first_name = models.CharField(_("first name"), max_length=_name_length, db_index=True)
    last_name = models.CharField(_("last name"), max_length=_name_length, db_index=True)
    middle_name = models.CharField(_("middle name"), max_length=_name_length, blank=True)

    date_of_birth = models.DateField(blank=True, null=True)

    club = models.ForeignKey("SportClub", blank=True, null=True, on_delete=models.SET_NULL)
    primary_group = models.ForeignKey("chanbara.GroupType", blank=True, null=True, on_delete=models.SET_NULL,
                                      limit_choices_to={"is_primary": True})

    chancode = models.CharField(max_length=16, unique=True, null=True, blank=True)
    # history = HistoricalRecords

    def save(self, *args, **kwargs):
        """ WARNING implement collision handling """
        if self.chancode is None:
            chancode = self.make_chancode()
            if chancode.is_filled:
                self.chancode = chancode.encode()
        super().save(*args, **kwargs)

    def make_chancode(self):
        return ChanCode(profile=self)

    @property
    def chancode_format(self):
        if self.chancode:
            return ChanCode.format_static(self.chancode)
        else:
            return "-"

    def html_profile_qr(self):
        if self.pk:
            site = Site.objects.latest("id")
            code = '{% load qr_code %}{% qr_from_text qr_body size="s" image_format="png" error_correction="m" %}'
            url = f"http://{site.domain}{self.get_absolute_url()}"
            context = Context({'qr_body': url})
            html = Template(code).render(context=context)
        else:
            html = "QR-code is not available yet"
        return html

    html_profile_qr.allow_tags = True
    html_profile_qr.short_description = "Profile QR"

    def get_absolute_url(self):
        return reverse('core:profile', kwargs={'chancode': self.chancode})

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
