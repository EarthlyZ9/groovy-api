import os
import requests
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured

load_dotenv()


def get_env_value(var_name, default=None):
    """help function for os.getenv to handle KeyError"""
    try:
        if default is not None:
            return os.getenv(var_name, default=default)
        else:
            return os.getenv(var_name)
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg) from None

def get_ec2_private_ip():
    try:
        return requests.get(
            'http://169.254.169.254/latest/meta-data/local-ipv4',
            timeout=0.01).text
    except requests.exceptions.RequestException:
        return None


DJANGO_SETTINGS_MODULE = get_env_value(
    "DJANGO_SETTINGS_MODULE", "config.settings.debug"
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)

EC2_PRIVATE_IP = get_ec2_private_ip()

# HOST NAME
HOST_NAME = get_env_value("HOST")
