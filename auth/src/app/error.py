from http import HTTPStatus

from api.v1.response_code import InvalidAPIUsage
from flask import json, jsonify
from logger import logger


def handle_exception(e):
    logger.info(e.description)
    error = InvalidAPIUsage("Something went wrong", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    return jsonify(error.to_dict()), error.status_code
