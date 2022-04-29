from datetime import datetime

from flask import request
from flask import Blueprint, jsonify, request, g
from flask_jwt_extended import (get_jwt_identity, get_jwt,  jwt_required, create_access_token)

from schemes.user import UserLoginSchema, UserRegisterSchema

from redis_db import redis_conn
from services.user import get_user_service as user_service
from services.account import get_account_service as account_service
from services.auth_token import get_auth_token_service as auth_token_service
from config import Config
from api.v1.response_code import InvalidAPIUsage

auth_api = Blueprint("auth_api", __name__)
config = Config()


# @auth_api.route("/login", methods=["POST"])
# def login():
#     """
#         Авторизация пользователя
#         ---
#         tags:
#           - Login API
#         parameters:
#           - name: login
#             in: path
#             type: string
#             required: true
#             description: The awesomeness list
#           - name: password
#             in: path
#             type: string
#             required: true
#             description: The awesomeness list
#         produces:
#         - application/json
#         responses:
#           500:
#             description: Ошибка!
#           200:
#             description: Успешно (Временно оставлю тут это- потом изменю)
#             application/json:
#                 schema:
#                   id: User
#                   properties:
#                     language:
#                       type: string
#                       description: The language name
#                       default: Lua
#                     features:
#                       type: array
#                       description: The awesomeness list
#                       items:
#                         type: string
#                       default: ["perfect", "simple", "lovely"]
#
#         """
#     login = request.json.get("login", None)
#     password = request.json.get("password", None)
#     admin = User(login=login, _password=password, email=login + "ddsd222@mail.ru")
#     db.session.add(admin)
#     db.session.commit()
#     print(User.query.all()[1]._password)
#
#     # if login != "test" or password != "test":
#     #     return jsonify({"msg": "Bad username or password"}), 401
#
#     access_token = create_access_token(identity=login)
#     return jsonify(access_token=access_token)


@auth_api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@auth_api.route("/login", methods=["POST"])
# TODO Необходимо прописать в документацию варианты ответов
# TODO Необходимо добавить файл yaml
# TODO Перенести message в constant
def login_view():
    data = request.json

    if not data:
        raise InvalidAPIUsage("Не верно предоставленны данные пользователя", status_code=400)

    login = data.get("login")
    password = data.get("password")

    try:
        UserLoginSchema().load({"login": login, "_password": password})
    except Exception as e:
        raise InvalidAPIUsage("Не верно предоставленны данные пользователя", status_code=400, payload={"error": str(e)})
    try:
        login = account_service.login(login=login, password=password, user_agent=request.user_agent)
    except Exception as e:
        raise InvalidAPIUsage("Что-то пошло не так", status_code=500, payload={"error": str(e)})
    if login:
        try:
            access, refresh = login
            return jsonify(access_token=access, refresh_token=refresh)

        except Exception as e:
            raise InvalidAPIUsage("Что-то пошло не так", status_code=500, payload={"error": str(e)})

    raise InvalidAPIUsage("Неверный логин или пароль", status_code=401)


@auth_api.route("/registration", methods=["POST"])
def registration_view():
    data = request.json

    if not data:
        raise InvalidAPIUsage("Необходимо предоставить данные пользователя", status_code=400)

    login = data.get("login")
    password = data.get("password")
    email = data.get("email")
    try:
        UserRegisterSchema().load({"login": login,
                                   "email": email,
                                   "_password": password})
    except Exception as e:
        raise InvalidAPIUsage("Не верно предоставленны данные", status_code=400, payload={"error": str(e)})

    is_existed_email = user_service.get_by_email(email)
    if is_existed_email:
        raise InvalidAPIUsage("Пользователь с таким email же зарегистрирован", status_code=400)

    is_existed_login = user_service.get_by_login(login)
    if is_existed_login:
        raise InvalidAPIUsage("Пользователь с таким login же зарегистрирован", status_code=400)

    user = user_service.create(login=login, email=email, password=password)
    if user:
        return jsonify(message="Registration Success")

    raise InvalidAPIUsage("Что-то пошло не так", status_code=500)


@auth_api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    # TODO ДОБАВИТЬ UPDATE REFRESH ТОКЕНА В БД
    return jsonify(access_token=access)


@auth_api.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    jti = get_jwt()["jti"]
    try:
        account_service.logout(user_id=user_id, jti=jti, user_agent=request.user_agent)
        return jsonify({"message": "Success logout."}), 200
    except Exception as e:
        return {
                   "message": "Something went wrong!",
                   "error": str(e),
                   "data": None
               }, 500


@auth_api.route("/full_logout", methods=["POST"])
@jwt_required()
def full_logout():
    user_id = get_jwt_identity()
    try:
        account_service.full_logout(user_id=user_id)
        return jsonify({"message": "Success logout."}), 200
    except Exception as e:
        return {
                   "message": "Something went wrong!",
                   "error": str(e),
                   "data": None
               }, 500

