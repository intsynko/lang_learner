import datetime
from datetime import timedelta
from typing import List

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.contrib.auth.hashers import check_password
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext_lazy as _


class User(auth_models.AbstractUser):
    STATUS_CREATED = "created"
    STATUS_ACTIVE = "active"
    STATUS_DISABLED = "disabled"
    STATUS_CHOICES = (
        (STATUS_CREATED, _("Created")),
        (STATUS_ACTIVE, _("Active")),
        (STATUS_DISABLED, _("Disabled")),
    )
    STATUS_CHOICES_DICT = dict(STATUS_CHOICES)

    email = models.EmailField(_("Email address"), blank=False)
    is_email_proved = models.BooleanField(_("Is email proved"), default=False)

    date_created = models.DateTimeField(_("Date account created"), auto_now_add=True, null=True)
    date_activated = models.DateTimeField(_("Date client received first bonus"), blank=True, null=True)
    date_disabled = models.DateTimeField(_("Date account was blocked"), blank=True, null=True)
    date_updated = models.DateTimeField(_("Date of last account update"), auto_now=True)

    status = models.CharField(_("Status"), max_length=16, choices=STATUS_CHOICES, default=STATUS_CREATED, db_index=True)
    language = models.CharField(_("Language"), max_length=5, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
