import os

from .common import *  # noqa
from .common import BASE_DIR

DEBUG = False

ALLOWED_HOSTS = [
    "ossia.ens.fr",
    "www.ossia.ens.fr",
    "ossia.pythonanywhere.com"
]

STATIC_URL = "https://ossia.pythonanywhere.com/static/"
STATIC_ROOT ="/home/ossia/Ossia/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media")
