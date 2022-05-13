import datetime
from http import HTTPStatus

from config import Config
from flask import Flask, g, jsonify, request
from jwt_extended import jwt
from redis_db import redis_conn, redis_rate_limit

config = Config()


def init_token_check(app: Flask):
    @app.before_request
    def is_valid_token():
        authorization = request.headers.get("Authorization")
        if authorization:
            g.access_token = authorization.split()[1]


def init_rate_limit(app: Flask):
    @app.before_request
    def rate_limit():
        pipe = redis_rate_limit.pipeline()
        now = datetime.datetime.now()
        key = f"{request.remote_addr}:{now.minute}"

        pipe.incr(key, 1)
        pipe.expire(key, config.RATE_LIMIT.TIME)

        result = pipe.execute()

        if result[0] > config.RATE_LIMIT.MAX_CALLS:
            return jsonify(
                message="you have exceeded the allowed number of requests"), HTTPStatus.TOO_MANY_REQUESTS


def init_check_request_id(app: Flask):
    @app.before_request
    def check_request():
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            return jsonify(message="request id is required"), HTTPStatus.BAD_REQUEST


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]

    user_id = jwt_payload["sub"]

    iat = jwt_payload["iat"]

    key_full_logout = f"full_logout_{user_id}"
    key = f"revoked_token_{jti}"

    full_logout = redis_conn.get(key_full_logout)

    if full_logout and iat < float(full_logout):

        token_in_redis = True

    else:

        token_in_redis = redis_conn.get(key)

    return token_in_redis is not None
