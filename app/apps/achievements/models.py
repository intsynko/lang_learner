from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.account import models as account_models
from apps.dictionary import models as dict_models


class Attempt(models.Model):
    user = models.ForeignKey(account_models.User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="attempts")
    dictionary = models.ForeignKey(dict_models.Dictionary, verbose_name=_("Dictionary"), on_delete=models.CASCADE, related_name="attempts")
    date = models.DateField(auto_now=True)
