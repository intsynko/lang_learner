import os

import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env = environ.Env(DEBUG=(bool, False), SECRET_KEY=(str, ""))
env.read_env(os.path.join(BASE_DIR, "../.env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY")
IS_PRODUCTION = bool(env("DJANGO_SETTINGS_MODULE") == "settings.production")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = [f"http://{host}" for host in ALLOWED_HOSTS]

ROOT_URLCONF = "urls"

WSGI_APPLICATION = "wsgi.application"

DATE_FORMATS = ["%Y.%m.%d", ]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
