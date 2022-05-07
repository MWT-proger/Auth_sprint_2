from http import HTTPStatus

from api.v1.base import BaseAPI
from api.v1.response_code import get_error_response as error_response
from api.v1.swag import account as swag
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, get_jwt, get_jwt_identity,
                                jwt_required)
from schemes.user import UserLoginSchema
from services.account import get_account_service as account_service
from services.auth_token import get_auth_token_service as auth_token_service

auth_api = Blueprint("auth_api", __name__)


class LoginView(BaseAPI):
    schema = UserLoginSchema()
    service = account_service

    @swag_from(swag.login_swagger)
    def post(self):
        data = self.get_data()
        if self.data_validation(data):
            login = data.get("login")
            password = data.get("_password")

            login = self.service.login(login=login, password=password, user_agent=request.user_agent)

            if login:
                access, refresh = login
                return jsonify(access_token=access, refresh_token=refresh)

            self.error("Wrong login or password", status_code=HTTPStatus.UNAUTHORIZED)


@auth_api.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@swag_from(swag.refresh_token_swagger)
def refresh_token():
    identity = get_jwt_identity()
    authorization = request.headers.get("Authorization")
    old_refresh = authorization.split()[1]

    new_refresh = auth_token_service.update_refresh_token(user_id=identity, refresh_token=old_refresh)

    if new_refresh:
        access = create_access_token(identity=identity)
        return jsonify(access_token=access, refresh_token=new_refresh)

    return error_response.error("Token has been revoked", status_code=HTTPStatus.UNAUTHORIZED)


@auth_api.route("/logout", methods=["POST"])
@jwt_required()
@swag_from(swag.logout_swagger)
def logout():
    user_id = get_jwt_identity()
    jti = get_jwt()["jti"]
    account_service.logout(user_id=user_id, jti=jti, user_agent=request.user_agent)
    return jsonify({"msg": "Success logout."})


@auth_api.route("/full_logout", methods=["POST"])
@jwt_required()
@swag_from(swag.full_logout_swagger)
def full_logout():
    user_id = get_jwt_identity()
    account_service.full_logout(user_id=user_id)
    return jsonify({"msg": "Success logout."})


@auth_api.route("/protected", methods=["GET"])
@jwt_required()
@swag_from(swag.protected_swagger)
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user)


auth_api.add_url_rule("/login", view_func=LoginView.as_view("login"), methods=["POST"])
