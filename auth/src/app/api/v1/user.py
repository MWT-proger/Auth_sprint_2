from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from flasgger import swag_from
from services.role import role_service
from api.v1.base import BaseAPI
from api.v1.response_code import get_error_response as error_response
from api.v1.swag import user as swag
from schemes.login_history import LoginHistorySchema
from schemes.user import UserRegisterSchema, UserUpdateSchema
from services.user import get_user_service as user_service
from http import HTTPStatus
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


@user_api.get("/roles/<user_id>")
@jwt_required()
def get_user_role(user_id):
    try:
        roles = role_service.get_user_role(user_id)
    except Exception as e:
        return error_response.error_500(str(e))
    return jsonify(roles=roles)


@user_api.post("/roles/<user_id>/<role_id>")
@jwt_required()
@check_role("admin")
def add_role(user_id, role_id):
    try:
        role_service.add_role_to_user(user_id, role_id)
    except Exception as e:
        return error_response.error_500(str(e))

    return jsonify(message="Role added successfully")


@user_api.delete("/roles/<user_id>/<role_id>")
@jwt_required()
@check_role("admin")
def delete_role(user_id, role_id):
    try:
        role_service.delete_role_from_user(user_id, role_id)
    except Exception as e:
        return error_response.error_500(str(e))

    return jsonify(message="Role deleted successfully")


@user_api.route("/my_login_history", methods=["GET"])
@jwt_required()
@swag_from(swag.get_login_history_swagger)
def get_login_history_view():
    current_user = get_jwt_identity()

    login_history, error = user_service.get_login_history(user_id=current_user)

    if not login_history:
        return error_response.error_500()

    return jsonify(LoginHistorySchema(many=True).dump(login_history))
