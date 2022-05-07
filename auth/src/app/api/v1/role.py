from http import HTTPStatus

from api.v1.base import BaseAPI
from api.v1.response_code import get_error_response as error_response
from api.v1.swag.role import get_roles, update_role, delete_role
from flasgger import swag_from
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from schemes.role import RoleCreateSchema, RoleUpdateSchema
from services.role import role_service
from utils.check_role import check_role

role_api = Blueprint("role_api", __name__)


class RoleView(BaseAPI):
    schema = RoleCreateSchema()
    service = role_service

    def service_work(self, data):
        try:
            role_id = role_service.create(data)
        except Exception as e:
            return error_response.error_500()

        return jsonify({"role_id": role_id, "message": "Роль успешно создана"}), HTTPStatus.OK

    @swag_from(get_roles)
    def get(self):
        try:
            roles = role_service.get_all()
        except Exception as e:
            return error_response.error_500()

        return jsonify({"data": roles})

    @swag_from(update_role)
    @jwt_required()
    @check_role("admin")
    def put(self, role_id):
        self.schema = RoleUpdateSchema()
        data = self.get_data()

        if self.data_validation(data):
            try:
                role = role_service.update(role_id=role_id, data=data)
            except Exception as e:
                return error_response.error_500(str(e))

            return jsonify(id=role.id), HTTPStatus.OK

    @swag_from(delete_role)
    @jwt_required()
    @check_role("admin")
    def delete(self, role_id):
        try:
            role_service.delete_by_id(role_id)
        except Exception as e:
            return error_response.error_500()

        return jsonify({"message": "Роль успешно удалена"})


view = RoleView.as_view("role_api")

role_api.add_url_rule("/create", view_func=view, methods=["POST"])
role_api.add_url_rule("/", view_func=view, methods=["GET"])
role_api.add_url_rule("/<role_id>", view_func=view, methods=["DELETE", "PUT"])
