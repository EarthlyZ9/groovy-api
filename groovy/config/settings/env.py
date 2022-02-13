import os
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

load_dotenv()


def get_env_value(var_name, default=None):
    """help function for os.getenv to handle KeyError"""
    try:
        if default != None:
            return os.getenv(var_name, default=default)
        else:
            return os.getenv(var_name)
    except KeyError:
        error_msg = "Set the {} environment variable".format(var_name)
        raise ImproperlyConfigured(error_msg) from None


DJANGO_SETTINGS_MODULE = get_env_value(
    "DJANGO_SETTINGS_MODULE", "config.settings.debug"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

# HOST NAME
HOST_NAME = get_env_value("HOST")
