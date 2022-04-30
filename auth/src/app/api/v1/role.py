from http import HTTPStatus

from flask import Blueprint, jsonify, request

from api.v1.response_code import InvalidAPIUsage
from services.role import role_service

role_api = Blueprint("role_api", __name__)


@role_api.post("/create")
def create():
    try:
        data = request.json
    except Exception as e:
        raise InvalidAPIUsage("Данные отсутствуют", status_code=HTTPStatus.BAD_REQUEST)

    if not data:
        raise InvalidAPIUsage("Не верно предоставленны данные", status_code=HTTPStatus.BAD_REQUEST)

    name = data.get("name")
    description = data.get("description")

    try:
        role_service.create(name, description)
    except Exception as e:
        raise InvalidAPIUsage("Ошибка базы данных", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    return jsonify({"message": "Роль успешно создана"}), HTTPStatus.OK


@role_api.get("/")
def get_all():
    try:
        roles = role_service.get_all()
    except Exception as e:
        raise InvalidAPIUsage("Ошибка базы данных", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    return jsonify({"data": roles})


@role_api.put("/<role_id>")
def update(role_id):
    pass


@role_api.delete("/<role_id>")
def delete(role_id):
    try:
        role_service.delete_by_id(role_id)
    except Exception as e:
        raise InvalidAPIUsage("Ошибка базы данных", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)

    return jsonify({"message": "Роль успешно удалена"})


@role_api.get("/user/<user_id>")
def get_user_role(user_id):
    pass


@role_api.put("/user/<user_id>")
def update_user_role(user_id):
    pass
