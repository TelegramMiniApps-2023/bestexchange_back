import os

from config import DB_USER, DB_PASS, DB_HOST, DB_NAME, DB_PORT, CSRF_TOKEN


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = CSRF_TOKEN

LANGUAGE_CODE = 'ru'

# TIME_ZONE = 'Europe/Moscow'

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    'debug_toolbar',

    "django_celery_beat",
    "general_models",
    "no_cash",
    "cash",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
     "127.0.0.1",
]

ROOT_URLCONF = "project.urls"

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
            ]
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # "NAME": "test_api_db",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASS,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_holder'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

#DEV
# STATIC_URL = "/django/static/"
# PROD
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PROJECT_NAME = "django-fastapi-project"

CELERY_IGNORE_RESULT = True

FASTAPI_PREFIX = "/api"
DJANGO_PREFIX = "/django"


####SWITCH FOR DEV/PROD####

# DEBUG = True
DEBUG = False

SITE_DOMAIN = 'wttonline.ru'
# SITE_DOMAIN = '127.0.0.1:81'

# ALLOWED_HOSTS = [SITE_DOMAIN]
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [f'https://{SITE_DOMAIN}']

CELERY_BROKER_URL='amqp://guest:guest@rabbitmq3:5672/'

PROTOCOL = 'https://'