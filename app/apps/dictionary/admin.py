from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


admin.site.register(models.Level, ModelAdmin)
admin.site.register(models.Tag, ModelAdmin)
admin.site.register(models.Rate, ModelAdmin)
admin.site.register(models.Language, ModelAdmin)
admin.site.register(models.Words, ModelAdmin)


class WordInline(admin.TabularInline):
    model = models.Words
    extra = 1


@admin.register(models.Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "name",
        "language_from",
        "language_to",
        "is_public",
        "is_active",
        "date_created",
    )

    readonly_fields = ("date_created",)

    fieldsets = (
        (
            _(""),
            {
                "fields": ["name", "owner", "language_from", "language_to", "is_public",
                           "is_active", "date_created", "level", "tags"],
            },
        ),
    )
    list_per_page = 20
    search_fields = ("name", "language_from__code", "language_to__code", "tags__name")
    list_filter = ("language_from", "language_to", "is_public", "is_active", "level")
    inlines = (WordInline,)
