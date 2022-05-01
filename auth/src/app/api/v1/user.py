from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from services.role import role_service
from api.v1.base import BaseAPI
from api.v1.response_code import InvalidAPIUsage
from schemes.login_history import LoginHistorySchema
from schemes.user import UserRegisterSchema, UserUpdateSchema
from services.user import get_user_service as user_service
from http import HTTPStatus

user_api = Blueprint("user_api", __name__)


class UserView(BaseAPI):
    schema = UserRegisterSchema()
    service = user_service

    def service_work(self, data):
        user, error = self.service.create(data=data)

        if error:
            self.error_basic(error.message, error.code)

        if user:
            return jsonify(message="Registration Success")

        self.error_500()

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = self.service.get_by_user_id(user_id)

        if not user:
            self.error_500()

        return jsonify(login=user.login, email=user.email)

    @jwt_required()
    def put(self):
        self.schema = UserUpdateSchema()
        data = self.get_data()
        if self.data_validation(data):
            user_id = get_jwt_identity()

            user, error = self.service.update(user_id=user_id, data=data)

            if error:
                self.error_basic(error.message, error.code)

            return jsonify(login=user.login, email=user.email)


user_view = UserView.as_view("user_api")

user_api.add_url_rule("/registration", view_func=user_view, methods=["POST"])
user_api.add_url_rule("/my", view_func=user_view, methods=["GET", "PUT"])


@user_api.get("/roles/<user_id>")
def get_user_role(user_id):
    try:
        roles = role_service.get_user_role(user_id)
    except Exception as e:
        raise InvalidAPIUsage("Database error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                              payload={"error": str(e)})
    return jsonify(roles=roles)


@user_api.post("/roles/<user_id>/<role_id>")
def add_role(user_id, role_id):
    try:
        role_service.add_role_to_user(user_id, role_id)
    except Exception as e:
        raise InvalidAPIUsage("Database error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                              payload={"error": str(e)})

    return jsonify(message="Role added successfully")


@user_api.delete("/roles/<user_id>/<role_id>")
def delete_role(user_id, role_id):
    try:
        role_service.delete_role_from_user(user_id, role_id)
    except Exception as e:
        raise InvalidAPIUsage("Database error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                              payload={"error": str(e)})

    return jsonify(message="Role deleted successfully")


@user_api.route("/my_login_history", methods=["GET"])
@jwt_required()
def get_login_history_view():
    current_user = get_jwt_identity()

    login_history, error = user_service.get_login_history(user_id=current_user)

    if error:
        InvalidAPIUsage(error.message, status_code=error.code)

    return jsonify(LoginHistorySchema(many=True).dump(login_history))
