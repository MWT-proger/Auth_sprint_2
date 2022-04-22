from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from flask import Blueprint

auth_api = Blueprint('auth_api', __name__)


@auth_api.route('/login', methods=["POST"])
def login():
    """
        Авторизация пользователя
        ---
        tags:
          - Login API
        parameters:
          - name: login
            in: path
            type: string
            required: true
            description: The awesomeness list
          - name: password
            in: path
            type: string
            required: true
            description: The awesomeness list
        produces:
        - application/json
        responses:
          500:
            description: Ошибка!
          200:
            description: Успешно (Временно оставлю тут это- потом изменю)
            application/json:
                schema:
                  id: User
                  properties:
                    language:
                      type: string
                      description: The language name
                      default: Lua
                    features:
                      type: array
                      description: The awesomeness list
                      items:
                        type: string
                      default: ["perfect", "simple", "lovely"]

        """
    login = request.json.get("login", None)
    password = request.json.get("password", None)
    if login != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=login)
    return jsonify(access_token=access_token)


@auth_api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



