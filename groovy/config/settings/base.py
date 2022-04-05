"""
Django settings for friggs idoctor project.
"""
import sys
import datetime
from pathlib import Path
from .env import get_env_value


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = get_env_value("DJANGO_SECRET_KEY")

DEBUG = True  # to be overridden

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]  # to be overridden


# Application definition

DJANGO_CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "drf_yasg",
    "rest_framework",
    "corsheaders",
    "django_extensions",
    "django_filters",
]
CODOT_APPS = [
    "user",
    "friend",
    "group",
    "chat",
]
INSTALLED_APPS = DJANGO_CORE_APPS + THIRD_PARTY_APPS + CODOT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTH_USER_MODEL = "user.User"

SITE_ID = 1

# CORS
CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "https://www.codot.site"]

ROOT_URLCONF = "config.urls"

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
        },
    },
]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": get_env_value("DB_HOST"),
        "PORT": get_env_value("DB_PORT"),
        "NAME": get_env_value("DB_NAME"),
        "USER": get_env_value("DB_USER"),
        "PASSWORD": get_env_value("DB_PASSWORD"),
        "CONN_MAX_AGE": 60 * 10,  # 10 minutes
        "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        "TEST": {"NAME": "test_db"},
    },
}

# Database for test
if "test" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.mysql",
        "HOST": get_env_value("TEST_DB_HOST"),
        "PORT": get_env_value("TEST_DB_PORT"),
        "NAME": get_env_value("TEST_DB_NAME"),
        "USER": get_env_value("TEST_DB_USER"),
        "PASSWORD": get_env_value("TEST_DB_PASSWORD"),
        "TEST": {"NAME": "test_db"},
    }

"""
# Cache
CACHE_LOCATION = "redis://localhost:6379/0"
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CACHE_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
"""


# use cache for Session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Redis configurations
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Django REST Framework configurations
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "config.exceptions.custom_exception_handler",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
    # "DEFAULT_RENDERER_CLASSES": [
    # 'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    # ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}


# Django REST Framework simpleJWT configurations
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(weeks=4),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(weeks=12),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": get_env_value("JWT_SECRET_KEY"),
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": get_env_value("HOST", None),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": datetime.timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": datetime.timedelta(days=1),
}


# drf-yasg configurations for swagger and redoc
SWAGGER_SETTINGS = {
    "DEFAULT_INFO": "config.urls.api_info",
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}


WSGI_APPLICATION = "config.wsgi.debug.application"

ASGI_APPLICATION = "config.asgi.application"


# Internationalization
LANGUAGE_CODE = "ko-KR"

USE_I18N = False

# Localization
USE_L10N = False

USE_THOUSAND_SEPARATOR = True

# Korean Time Applied
USE_TZ = False

TIME_ZONE = "Asia/Seoul"


# Max upload size
DATA_UPLOAD_MAX_MEMORY_SIZE = 12 * 1024 * 1024  # 12MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 12 * 1024 * 1024  # 12MB


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/assets/"
STATIC_ROOT = BASE_DIR / "assets"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# media files
MEDIA_URL = "/uploads/"
MEDIA_ROOT = BASE_DIR / "uploads"
