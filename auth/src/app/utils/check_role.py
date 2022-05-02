from functools import wraps
from http import HTTPStatus

from api.v1.response_code import InvalidAPIUsage
from flask_jwt_extended import get_jwt_identity
from services.user import get_user_service as user_service


def check_role(role):
    def wrapper(func):
        @wraps(func)
        def decorate_view(*args, **kwargs):
            user = user_service.get_by_user_id(get_jwt_identity())

            if user.has_role(role):
                return func(*args, **kwargs)

            raise InvalidAPIUsage("You don't have enough rights", status_code=HTTPStatus.BAD_REQUEST)

        return decorate_view

    return wrapper
