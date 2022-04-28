from flask import Flask
from flask import request, g, jsonify
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
    token_in_redis = redis_conn.get(jti)
    print('token_in_redis')
    print(token_in_redis)
    return token_in_redis is not None
