from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt, get_jwt_identity,
                                jwt_required)
from flasgger import swag_from

from api.v1.base import BaseAPI
from api.v1.response_code import InvalidAPIUsage
from api.v1.swag.account import login_swagger
from schemes.user import UserLoginSchema
from services.account import get_account_service as account_service
from services.auth_token import get_auth_token_service as auth_token_service

auth_api = Blueprint("auth_api", __name__)

# TODO Необходимо прописать в документацию варианты ответов
# TODO Необходимо добавить файл yaml
# TODO Перенести message в constant


class LoginView(BaseAPI):
    schema = UserLoginSchema()
    service = account_service

    @swag_from(login_swagger)
    def post(self):
        data = self.get_data()
        if self.data_validation(data):
            login = data.get("login")
            password = data.get("_password")
            try:
                login = self.service.login(login=login, password=password, user_agent=request.user_agent)
            except Exception as e:
                self.error_500(str(e))
            if login:
                try:
                    access, refresh = login
                    return jsonify(access_token=access, refresh_token=refresh)
                except Exception as e:
                    self.error_500(str(e))
            self.error_basic("Неверный логин или пароль", 401)


auth_api.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=["POST"])


@auth_api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    authorization = request.headers.get("Authorization")
    old_refresh = authorization.split()[1]

    new_refresh = auth_token_service.update_refresh_token(user_id=identity, refresh_token=old_refresh)

    if new_refresh:
        access = create_access_token(identity=identity)
        return jsonify(access_token=access, refresh_token=new_refresh)

    raise InvalidAPIUsage("Token has been revoked", status_code=401)


@auth_api.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    jti = get_jwt()["jti"]
    try:
        account_service.logout(user_id=user_id, jti=jti, user_agent=request.user_agent)
        return jsonify({"message": "Success logout."})
    except Exception as e:
        raise InvalidAPIUsage("Что-то пошло не так", status_code=500, payload={"error": str(e)})


@auth_api.route("/full_logout", methods=["POST"])
@jwt_required()
def full_logout():
    user_id = get_jwt_identity()
    try:
        account_service.full_logout(user_id=user_id)
        return jsonify({"message": "Success logout."})
    except Exception as e:
        raise InvalidAPIUsage("Что-то пошло не так", status_code=500, payload={"error": str(e)})


@auth_api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)
