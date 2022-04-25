from flask import Flask
from flask import request, g, jsonify
from services.storage import token_storage


def init_token_check(app: Flask):
    @app.before_request
    def is_valid_token():
        authorization = request.headers.get("Authorization")
        if authorization:
            g.access_token = authorization.split()[1]
            if not token_storage.is_valid_access(g.access_token):
                return jsonify({"message": "Invalid access token"}), 400
