from flask import Flask, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, create_refresh_token
from flask import Blueprint

from database import db
from models import User
from services.user import UserService
from schemes.user import UserRegisterSchema, UserLoginSchema
from utils.validate import validate_login_and_password

auth_api = Blueprint("auth_api", __name__)
user_service = UserService()


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

        try:
            UserLoginSchema().load({"login": login, "_password": password})
        except Exception as e:
            return {
                       "message": "Пожалуйста, предоставьте данные пользователя",
                       "error": str(e),
                       "data": None
                   }, 400
        print(33)
        user = user_service.login(login=login, password=password)
        print(43)
        if user:
            try:
                # TODO Необходимо добавить Login History
                # TODO Необходимо сохранять в Redis token
                # TODO Необходимо проверять существует ли refresh (надо ли его тогда пересоздавать)
                access_token = create_access_token(identity="example_user", fresh=True)
                refresh_token = create_refresh_token(identity="example_user")
                return jsonify(access_token=access_token, refresh_token=refresh_token)
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500

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
                   }, 404

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

