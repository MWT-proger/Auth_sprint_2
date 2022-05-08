from flask import Flask, g, jsonify, request
from jwt_extended import jwt

from redis_db import redis_conn


def init_token_check(app: Flask):
    @app.before_request
    def is_valid_token():
        authorization = request.headers.get("Authorization")
        if authorization:
            g.access_token = authorization.split()[1]


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
