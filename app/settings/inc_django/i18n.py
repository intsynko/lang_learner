import os

from django.utils.translation import gettext_lazy as _

from ..base import BASE_DIR

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en"
LANGUAGES = (
    ("ru", _("Russian")),
    ("en", _("English")),
)
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale/")]

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True
