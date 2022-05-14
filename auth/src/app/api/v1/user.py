from api.v1.base import BaseAPI
from api.v1.response_code import get_error_response as error_response
from api.v1.swag import user as swag
from api.v1.swag.role import add_role, get_user_role, remove_role
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from schemes.login_history import LoginHistorySchema
from schemes.user import (UserChangePasswordSchema, UserRegisterSchema,
                          UserUpdateSchema)
from services.role import role_service
from services.user import get_user_service as user_service
from utils.check_role import check_role

user_api = Blueprint("user_api", __name__)


class UserView(BaseAPI):
    schema = UserRegisterSchema()
    service = user_service

    @swag_from(swag.signup_swagger)
    def post(self):
        data = self.get_data()
        if self.data_validation(data):
            user, error = self.service.create(data=data)

            if not user:
                return self.error_500()

            return jsonify(msg="Registration Success")

    @jwt_required()
    @swag_from(swag.user_me_swagger)
    def get(self):
        user_id = get_jwt_identity()
        user = self.service.get_by_user_id(user_id)

        if not user:
            return self.error_500()

        return jsonify(login=user.login, email=user.email)

    @jwt_required()
    @swag_from(swag.update_user_swagger)
    def put(self):
        self.schema = UserUpdateSchema()
        data = self.get_data()
        if self.data_validation(data):
            user_id = get_jwt_identity()

            user, error = self.service.update(user_id=user_id, data=data)

            if not user:
                return self.error_500()

            return jsonify(login=user.login, email=user.email)


user_view = UserView.as_view("user_api")

user_api.add_url_rule("/registration", view_func=user_view, methods=["POST"])
user_api.add_url_rule("/my", view_func=user_view, methods=["GET", "PUT"])


class ChangePassword(BaseAPI):
    schema = UserChangePasswordSchema()
    service = user_service

    @jwt_required()
    @swag_from(swag.change_password_user_swagger)
    def put(self):
        data = self.get_data()
        if self.data_validation(data):
            user_id = get_jwt_identity()

            self.service.change_password(user_id=user_id, data=data)

            return jsonify(msg="Password successfully changed")


change_password = ChangePassword.as_view("change_password")

user_api.add_url_rule("/change_password", view_func=change_password, methods=["PUT"])


@user_api.get("/roles/<user_id>")
@jwt_required()
@swag_from(get_user_role)
def get_user_role(user_id):
    roles = role_service.get_user_role(user_id)

    return jsonify(roles=roles)


@user_api.post("/roles/<user_id>/<role_id>")
@jwt_required()
@check_role("admin")
@swag_from(add_role)
def add_role(user_id, role_id):
    role_service.add_role_to_user(user_id, role_id)
    return jsonify(message="Role added successfully")


@user_api.delete("/roles/<user_id>/<role_id>")
@jwt_required()
@check_role("admin")
@swag_from(remove_role)
def delete_role(user_id, role_id):
    role_service.delete_role_from_user(user_id, role_id)

    return jsonify(message="Role deleted successfully")


@user_api.route("/my_login_history", methods=["GET"])
@jwt_required()
@swag_from(swag.get_login_history_swagger)
def get_login_history_view():
    current_user = get_jwt_identity()

    page = request.args.get("page", default=1, type=int)
    size = request.args.get("size", default=5, type=int)
    since = page * size - size

    login_history, error = user_service.get_login_history(user_id=current_user)

    docs = LoginHistorySchema(many=True).dump(login_history)

    return jsonify(docs[since:since + size])
