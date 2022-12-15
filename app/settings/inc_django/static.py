# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
import os

from settings.base import BASE_DIR

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "../static/")
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
