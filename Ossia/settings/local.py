import os

from .common import *  # noqa
from .common import BASE_DIR, INSTALLED_APPS, MIDDLEWARE

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEBUG = True

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

STATIC_URL = "/static/"
STATIC_ROOT = "static"
MEDIA_URL = "/media/"
MEDIA_ROOT = "media"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
