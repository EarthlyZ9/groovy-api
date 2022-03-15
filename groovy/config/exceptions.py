from django.contrib.auth import get_user_model
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

User = get_user_model()


class InvalidAuthRequestError(APIException):
    status_code = 400
    default_detail = "Given auth code or token is not valid."
    default_code = "invalid_auth_token"


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # check that a ValidationError exception is raised
    if isinstance(exc, InvalidAuthRequestError):
        pass

    return response
