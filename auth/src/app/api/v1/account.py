from flask import Blueprint, jsonify, request, g
from flask_jwt_extended import (get_jwt_identity, jwt_required, create_access_token)
from schemes.user import UserLoginSchema, UserRegisterSchema
from services.user import UserService
from services.account import AccountService
from services.storage import token_storage
from config import Config

auth_api = Blueprint("auth_api", __name__)
user_service = UserService()
account_service = AccountService()
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
        print(33)
        user = user_service.login(login=login, password=password)
        print(43)
        if user:
            try:
                # TODO Необходимо добавить Login History
                # TODO Необходимо сохранять в Redis token
                # TODO Необходимо проверять существует ли refresh (надо ли его тогда пересоздавать)
                access, refresh = account_service.get_tokens_pair(user.id)
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

    return jsonify(access_token=access)


@auth_api.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # TODO ДОБАВИТЬ УДАЛЕНИЕ REFRESH ТОКЕНА ИЗ БАЗЫ
    user_id = get_jwt_identity()
    token_storage.add_invalid_access(g.access_token, user_id, config.JWT.ACCESS_EXPIRE)
    return jsonify({"message": "Success logout."}), 200
