from flask import jsonify, Blueprint

bp_errors = Blueprint('errors', __name__)


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@bp_errors.app_errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code


class ResponseErrorApi:
    invalid_class = InvalidAPIUsage

    def __init__(self):
        pass

    def error_500(self, e: str = None):
        if e:
            raise self.invalid_class("Что-то пошло не так", status_code=500, payload={"error": e})
        raise self.invalid_class("Что-то пошло не так", status_code=500)

    def error_400(self, e):
        raise self.invalid_class("Не верно предоставленны данные", status_code=400, payload={"error": e})

    def error_basic(self, message, code, error: str = None):
        raise self.invalid_class(message, status_code=code, payload={"error": error})
