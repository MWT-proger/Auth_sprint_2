from flask import Blueprint, jsonify

bp_errors = Blueprint('errors', __name__)


class InvalidAPIUsage(Exception):
    status_code = 400
    status = "error"

    def __init__(self, message, status_code=None, payload=None, status: str = None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if status is not None:
            self.status = status

        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['status'] = self.status
        if self.status == "fail":
            rv['data'] = self.message
        else:
            rv['msg'] = self.message
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
            raise self.invalid_class("Something went wrong", status_code=500, payload={"data": e})
        raise self.invalid_class("Something went wrong", status_code=500)

    def error_400(self, e):
        raise self.invalid_class("The data is incorrect", status_code=400, payload={"data": e})

    def error_basic(self, message, code, error: str = None):
        raise self.invalid_class(message, status_code=code, payload={"data": error})

    def fail(self, message, status_code):
        raise self.invalid_class(message, status_code=status_code, status='fail')

    def error(self, message, status_code):
        raise self.invalid_class(message, status_code=status_code)

    def error_detail(self, message, status_code, detail):
        raise self.invalid_class(message, status_code=status_code, payload={"data": detail})


get_error_response = ResponseErrorApi()

