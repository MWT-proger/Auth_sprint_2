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
    try:
        data = request.json

        if not data:
            return {
                       "message": "Пожалуйста, предоставьте данные пользователя",
                       "data": None,
                       "error": "Bad request"
                   }, 400

        login = data.get("login")
        password = data.get("password")
        print(login)
        print(password)

        try:
            UserLoginSchema().load({"login": login, "_password": password})
        except Exception as e:
            return {
                       "message": "Пожалуйста, предоставьте данные пользователя",
                       "error": str(e),
                       "data": None
                   }, 400
        login = account_service.login(login=login, password=password, user_agent=request.user_agent)
        if login:
            try:
                # + Необходимо добавить Login History
                # + Необходимо сохранять в Redis token
                # + Необходимо проверять существует ли refresh (надо ли его тогда пересоздавать)
                access, refresh = login
                return jsonify(access_token=access, refresh_token=refresh)

            except Exception as e:
                return {
                           "error": "Something went wrong",
                           "message": str(e)
                       }, 500

        return {
                   "message": "Error fetching auth token!, invalid email or password",
                   "data": None,
                   "error": "Unauthorized"
               }, 401

    except Exception as e:
        return {
                   "message": "Something went wrong!",
                   "error": str(e),
                   "data": None
               }, 500


@auth_api.route("/registration", methods=["POST"])
def registration_view():
    try:
        data = request.json

        if not data:
            return {
                       "message": "Пожалуйста, предоставьте данные пользователя",
                       "data": None,
                       "error": "Bad request"
                   }, 400

        login = data.get("login")
        password = data.get("password")
        email = data.get("email")
        try:
            UserRegisterSchema().load({"login": login,
                                       "email": email,
                                       "_password": password})
        except Exception as e:
            return {
                       "message": "Пожалуйста, предоставьте данные пользователя",
                       "error": str(e),
                       "data": None
                   }, 400

        is_existed_email = user_service.get_by_email(email)
        if is_existed_email:
            return dict(message="Invalid data", data=None, error="Пользователь с таким email же зарегистрирован"), 400

        is_existed_login = user_service.get_by_login(login)
        if is_existed_login:
            return dict(message="Invalid data", data=None, error="Пользователь с таким login же зарегистрирован"), 400

        user = user_service.create(login=login, email=email, password=password)
        if user:
            return {
                       "message": "Registration Success",
                   }, 200

        return {
                   "message": "Error fetching auth token!, invalid email or password",
                   "data": None,
                   "error": "Unauthorized"
               }, 404

    except Exception as e:
        return {
                   "message": "Something went wrong!",
                   "error": str(e),
                   "data": None
               }, 500


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
# TODO Повторить logout, только для всех устройств
