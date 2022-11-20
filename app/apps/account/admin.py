from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.User)
class UserAdmin(_UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "status",
        "is_staff",
        "is_superuser",
        "date_created",
    )

    fieldsets = _UserAdmin.fieldsets + (
        (
            _("Profile"),
            {
                "fields": ["status", ],
            },
        ),
    )
    list_per_page = 20
    search_fields = ("username", "first_name", "last_name", "email")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "status")

