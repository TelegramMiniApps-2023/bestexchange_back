import os

import sentry_sdk

from config import (DB_USER,
                    DB_PASS,
                    DB_HOST,
                    DB_NAME,
                    DB_PORT,
                    CSRF_TOKEN,
                    REDIS_URL)


sentry_sdk.init(
    dsn="https://092663a7578a856b241d61d8c326be00@o4506694926336000.ingest.sentry.io/4506739040190464",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = CSRF_TOKEN

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_TZ = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    'debug_toolbar',
    "django_celery_beat",
    'django_summernote',

    "general_models",
    "no_cash",
    "cash",
    "partners",
    'seo_admin'
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
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
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

PROTOCOL = 'https://'

CSRF_TRUSTED_ORIGINS = [f'{PROTOCOL}{SITE_DOMAIN}']

#RabbitMQ  PROD
# CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq3:5672/'

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

X_FRAME_OPTIONS = 'SAMEORIGIN'