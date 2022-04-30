from flask import Blueprint, jsonify
from api.v1.response_code import InvalidAPIUsage
from services.role import role_service
from http import HTTPStatus
from schemes.role import RoleCreateSchema, RoleUpdateSchema
from api.v1.base import BaseAPI

role_api = Blueprint("role_api", __name__)


class RoleView(BaseAPI):
    schema = RoleCreateSchema()
    service = role_service

    def service_work(self, data):
        try:
            role_id = role_service.create(data)
        except Exception as e:
            raise InvalidAPIUsage("Ошибка базы данных", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        return jsonify({"role_id": role_id, "message": "Роль успешно создана"}), HTTPStatus.OK

    def get(self):
        try:
            roles = role_service.get_all()
        except Exception as e:
            raise InvalidAPIUsage("Ошибка базы данных", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        return jsonify({"data": roles})

    def put(self, role_id):
        self.schema = RoleUpdateSchema()
        data = self.get_data()

        if self.data_validation(data):
            role = role_service.update(role_id=role_id, data=data)

            return jsonify(id=role.id), HTTPStatus.OK

    def delete(self, role_id):
        try:
            role_service.delete_by_id(role_id)
        except Exception as e:
            raise InvalidAPIUsage("Ошибка базы данных", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

        return jsonify({"message": "Роль успешно удалена"})


view = RoleView.as_view("role_api")

role_api.add_url_rule("/create", view_func=view, methods=["POST"])
role_api.add_url_rule("/", view_func=view, methods=["GET"])
role_api.add_url_rule("/<role_id>", view_func=view, methods=["DELETE", "PUT"])


@role_api.put("/user/<user_id>")
def update_user_role(user_id):
    pass
