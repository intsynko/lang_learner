import uuid
from io import BytesIO
from typing import List

from gtts import gTTS
from django.db import models
from django.db.models import Count, Avg, Q
from django.utils.translation import gettext_lazy as _
from django.core.files.base import ContentFile


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


class LearningMode(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    code = models.CharField(_("Code"), max_length=50)

    def __str__(self):
        return self.name


class Dictionary(models.Model):
    language_from = models.ForeignKey(Language, verbose_name=_("Language from"),
                                      on_delete=models.PROTECT, related_name="dicts_to")
    language_to = models.ForeignKey(Language, verbose_name=_("Language to"),
                                    on_delete=models.PROTECT, related_name="dicts_from")
    name = models.CharField(_("Name"), max_length=50)
    owner = models.ForeignKey("account.User", verbose_name=_("Owner"), on_delete=models.PROTECT,
                              related_name="dicts")
    date_created = models.DateField(_("Date"), auto_now=True)
    pinned = models.ManyToManyField("account.User", verbose_name=_("Pinned"),
                                    related_name="dicts_pinned")
    learning_mods = models.ManyToManyField(LearningMode, verbose_name=_("Learning mods"),
                                           related_name="dicts")

    is_public = models.BooleanField(_("Is public"), default=True)
    tags = models.ManyToManyField(to=Tag, blank=True, verbose_name=_("Tags"), related_name="dicts")
    level = models.ForeignKey(Level, verbose_name=_("Level"), on_delete=models.PROTECT,
                              related_name="dicts")
    is_active = models.BooleanField(_("Is active"), default=True)
    session_count = models.IntegerField(_("Session count"), default=0)

    @classmethod
    def active(cls):
        return cls.objects.filter(is_active=True)

    @classmethod
    def queryset_wit_rating(cls):
        return cls.active().annotate(
            rates_cnt=Count("rates"),
            average_rate=Avg("rates__amount")
        )

    @classmethod
    def my(cls, user):
        return cls.queryset_wit_rating().filter(Q(owner=user) | Q(pinned__id=user.id))

    @classmethod
    def get_top(cls, search: str = None, amount: int = 10, lang: str = None,
                level: str = None, tag: str = None, tags: List[str] = None, **kwargs):
        queryset = cls.queryset_wit_rating()

        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(tags__name__icontains=search))

        if lang:
            queryset = queryset.filter(Q(language_from__code=lang) | Q(language_to__code=lang))

        if level:
            queryset = queryset.filter(level__name=level)

        if tag:
            queryset = queryset.filter(tags__name=tag)

        if tags:
            queryset = queryset.filter(tags__name__in=tags)

        return queryset.order_by("rates_cnt", "average_rate")[:amount]

    def __str__(self):
        return f"{self.name} [{self.language_from.code}-{self.language_to.code}] ({self.owner.email})"


class Rate(models.Model):
    amount = models.PositiveSmallIntegerField(_("Amount"))
    dictionary = models.ForeignKey(Dictionary, verbose_name=_("Dictionary"),
                                   on_delete=models.CASCADE, related_name="rates")
    user = models.ForeignKey("account.User", verbose_name=_("User"), on_delete=models.CASCADE,
                             related_name="rates")
    date_created = models.DateField(_("Date"), auto_now=True)

    def __str__(self):
        return f"{self.dictionary.name} ({self.owner.email}): {self.amount}"

    class Meta:
        unique_together = (("user", "dictionary"),)


class Words(models.Model):
    image = models.ImageField(upload_to='words/', null=True, blank=True)
    prononsiation = models.FileField(upload_to='words_prononsiation/', null=True, blank=True)
    dictionary = models.ForeignKey(Dictionary, verbose_name=_("Dictionary"),
                                   on_delete=models.CASCADE, related_name="words")
    word_from = models.CharField(_("Word from"), max_length=50, default="")
    word_to = models.CharField(_("Word from"), max_length=50, default="")
    active = models.BooleanField(default=True)
    example_1 = models.CharField(_("Example 1"), max_length=255, null=True, blank=True, default="")
    example_2 = models.CharField(_("Example 2"), max_length=255, null=True, blank=True, default="")
    frequency = models.SmallIntegerField(_("Frequency"), default=10)
    transcription = models.CharField(_("Transcription"), max_length=100, null=True, blank=True,
                                     default="")

    def load_prononsiation(self):
        audio = gTTS(self.word_from, lang=self.dictionary.language_from.code)
        obj = BytesIO()
        audio.write_to_fp(obj)
        obj.seek(0)
        self.prononsiation.save(f"{self.word_from}_{uuid.uuid4()}.mp3", ContentFile(obj.read()))
