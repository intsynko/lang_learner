from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.Attempt)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "dictionary",
        "date"
    )

    fieldsets = (
        (
            _(""),
            {
                "fields": ["user", "dictionary", "date"],
            },
        ),
    )
    raw_id_fields = ("user", "dictionary")
