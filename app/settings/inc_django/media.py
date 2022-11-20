import os

from ..base import BASE_DIR

MEDIA_ROOT = os.path.join(BASE_DIR, "../media/")
MEDIA_ROOT_PUBLIC = os.path.join(MEDIA_ROOT, "public/")
MEDIA_URL = "/media/"


ASSETS_ROOT = os.path.join(BASE_DIR, "apps/web/assets/")
ASSETS_URL = "/assets/"
