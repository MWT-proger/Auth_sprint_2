from http import HTTPStatus

from flask import jsonify, json

from api.v1.response_code import InvalidAPIUsage


def handle_exception(e):
    error = InvalidAPIUsage("Something went wrong", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    return jsonify(error.to_dict()), error.status_code
