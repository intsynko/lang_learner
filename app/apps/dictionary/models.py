
from django.db import models
from django.db.models import Count, Avg, Q
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    code = models.CharField(_("Code"), max_length=10)
    icon = models.ImageField(upload_to='icons', null=True)

    def __str__(self):
        return self.code


class Tag(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(_("Name"), max_length=10)

    def __str__(self):
        return self.name


class Dictionary(models.Model):
    language_from = models.ForeignKey(Language, verbose_name=_("Language from"), on_delete=models.PROTECT, related_name="dicts_to")
    language_to = models.ForeignKey(Language, verbose_name=_("Language to"), on_delete=models.PROTECT, related_name="dicts_from")
    name = models.CharField(_("Name"), max_length=50)
    owner = models.ForeignKey("account.User", verbose_name=_("Owner"), on_delete=models.PROTECT, related_name="dicts")
    date_created = models.DateField(_("Date"), auto_now=True)
    pinned = models.ManyToManyField("account.User", verbose_name=_("Pinned"), related_name="dicts_pinned")

    is_public = models.BooleanField(_("Is public"), default=True)
    tags = models.ManyToManyField(to=Tag, blank=True, verbose_name=_("Tags"), related_name="dicts")
    level = models.ForeignKey(Level, verbose_name=_("Level"), on_delete=models.PROTECT, related_name="dicts")

    @classmethod
    def queryset_wit_rating(cls):
        return cls.objects.annotate(
            rates_cnt=Count("rates"),
            average_rate=Avg("rates__amount")
        )

    @classmethod
    def my(cls, user):
        return cls.queryset_wit_rating().filter(Q(owner=user) | Q(pinned__id=user.id))

    @classmethod
    def get_top(cls, search: str = None, amount: int = 10, lang_from: str = None, lang_to: str = None, level: str = None):
        queryset = cls.queryset_wit_rating()

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(tag__name__icontains=search))

        if lang_from:
            queryset = queryset.filter(lang_from__code=lang_from)
        if lang_to:
            queryset = queryset.filter(lang_to__code=lang_to)

        if level:
            queryset = queryset.filter(level__name=level)

        return queryset.order_by("rates_cnt", "average_rate")[:amount]

    def __str__(self):
        return f"{self.name} [{self.language_from.code}-{self.language_to.code}] ({self.owner.email})"


class Rate(models.Model):
    amount = models.PositiveSmallIntegerField(_("Amount"))
    dictionary = models.ForeignKey(Dictionary, verbose_name=_("Dictionary"), on_delete=models.CASCADE, related_name="rates")
    user = models.ForeignKey("account.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="rates")
    date_created = models.DateField(_("Date"), auto_now=True)

    def __str__(self):
        return f"{self.dictionary.name} ({self.owner.email}): {self.amount}"

    class Meta:
        unique_together = (("user", "dictionary"),)
