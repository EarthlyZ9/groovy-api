# pylint: skip-file
from .env import EC2_PRIVATE_IP, HOST_NAME, API_HOST_NAME

WSGI_APPLICATION = "config.wsgi.deploy.application"

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost", HOST_NAME, API_HOST_NAME]

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)

SESSION_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[DJANGO] %(levelname)s %(asctime)s %(module)s "
            "%(name)s.%(funcName)s:%(lineno)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "daphne": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}
