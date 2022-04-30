from datastore import datastore
from database import session_scope
from models import Role
from http import HTTPStatus
from api.v1.response_code import InvalidAPIUsage
from services.user import get_user_service as user_service


class RoleService:
    def __init__(self):
        self.model = Role

    def create(self, data: dict):
        name = data.get("name")
        description = data.get("description")

        with session_scope() as session:
            role = datastore.create_role(name=name, description=description)
            session.add(role)
        return role.id

    def get_all(self):
        return [role.serialize() for role in self.model.query.all()]

    def update(self, role_id, data: dict):
        name = data.get("name")
        description = data.get("description")

        role = self.model.query.filter_by(id=role_id).first()

        if not name and not description:
            InvalidAPIUsage("Пользователь с таким login же зарегистрирован", status_code=HTTPStatus.BAD_REQUEST)

        with session_scope():
            if name and name != role.name:
                self.check_exists_name(name)
                role.name = name

            if description and description != role.description:
                role.description = description

        return role

    def check_exists_name(self, name):
        role = self.get_by_name(name)
        if role:
            raise InvalidAPIUsage("Role with this name already exist", status_code=400)

    def get_by_name(self, name):
        role = self.model.query.filter_by(name=name).first()
        return role

    def delete_by_id(self, id):
        with session_scope():
            self.model.query.filter_by(id=id).delete()

    def get_user_role(self, user_id):
        user = user_service.get_by_user_id(user_id)
        roles = [role.serialize() for role in user.roles]
        return roles


role_service: RoleService = RoleService()
