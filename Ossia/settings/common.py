import os

from django.utils.translation import gettext_lazy as _

try:
    from . import secret
except ImportError:
    raise ImportError(
        "The secret.py file is missing.\n"
        "For a development environment, simply copy secret_example.py"
    )


def import_secret(name):
    """
    Shorthand for importing a value from the secret module and raising an
    informative exception if a secret is missing.
    """
    try:
        return getattr(secret, name)
    except AttributeError:
        raise RuntimeError("Secret missing: {}".format(name))


SECRET_KEY = import_secret("SECRET_KEY")
ADMINS = import_secret("ADMINS")
SERVER_EMAIL = import_secret("SERVER_EMAIL")

DBNAME = import_secret("DBNAME")
DBUSER = import_secret("DBUSER")
DBPASSWD = import_secret("DBPASSWD")

ACCOUNT_CREATION_PASS = import_secret("ACCOUNT_CREATION_PASS")

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..")

INSTALLED_APPS = [
    "trombonoscope",
    "actu",
    "colorful",
    "calendrier",
    "gestion.apps.GestionConfig",
    "partitions.apps.PartitionsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "avatar",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "Ossia.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {
                "changelang": "gestion.templatetags.changelang",
                "modulo": "gestion.templatetags.modulo",
                "autotranslate": "gestion.templatetags.autotranslate",
                "halflength": "gestion.templatetags.halflength",
            },
        },
    }
]

WSGI_APPLICATION = "Ossia.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# I18n
# I18n
LANGUAGE_CODE = "fr"
LANGUAGES = (
    ("fr", _("Français")),
    ("en", _("English")),
)
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


AUTH_PROFILE_MODEL = "gestion.OssiaUser"

LOGIN_URL = "/login"

AVATAR_CLEANUP_DELETED = True
AVATAR_AUTO_GENERATE_SIZES = (250,)
AVATAR_CHANGE_TEMPLATE = "trombonoscope/change_avatar.html"
AVATAR_MAX_AVATARS_PER_USER = 1
AVATAR_EXPOSE_USERNAMES = False
AVATAR_STORAGE_DIR = "trombonoscope"
AVATAR_ADD_TEMPLATE = "trombonoscope/add_avatar.html"
AVATAR_DELETE_TEMPLATE = "trombonoscope/delete_avatar.html"
AVATAR_DEFAULT_URL = "Ossia"
AVATAR_PROVIDERS = (
    "avatar.providers.PrimaryAvatarProvider",
    "avatar.providers.DefaultAvatarProvider",
)
AVATAR_THUMB_FORMAT = "JPEG"
