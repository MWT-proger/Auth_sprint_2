from http import HTTPStatus

from api.v1.response_code import get_error_response as error_response
from database import session_scope
from datastore import datastore
from models import Role
from services.user import get_user_service as user_service
from sqlalchemy.exc import IntegrityError


class RoleDuplication(Exception):
    pass


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

        role = self.get_role_by_id(role_id)

        if not name and not description:
            return error_response.error_400()

        try:
            with session_scope():
                if name and name != role.name:
                    role.name = name

                if description and description != role.description:
                    role.description = description
        except IntegrityError as e:
            raise RoleDuplication("Role with this name already exist")

        return role

    def check_exists_name(self, name):
        role = self.get_by_name(name)
        if role:
            return error_response.fail({"name": "Role with this name already exist"}, status_code=HTTPStatus.BAD_REQUEST)

    def get_by_name(self, name):
        role = self.model.query.filter_by(name=name).first()
        return role

    def delete_by_id(self, id):
        with session_scope():
            self.model.query.filter_by(id=id).delete()

    def get_role_by_id(self, role_id):
        role = self.model.query.filter_by(id=role_id).first()
        return role

    def get_user_role(self, user_id):
        user = user_service.get_by_user_id(user_id)
        roles = [role.serialize() for role in user.roles]
        return roles

    def add_role_to_user(self, user_id, role_id):
        user = user_service.get_by_user_id(user_id)
        role = self.get_role_by_id(role_id)

        if not user:
            return error_response.fail("User with this id not found",
                                       status_code=HTTPStatus.BAD_REQUEST)

        if not role:
            return error_response.fail("Role with this id not found",
                                       status_code=HTTPStatus.BAD_REQUEST)

        if user.has_role(role):
            return error_response.fail("User already has this role",
                                       status_code=HTTPStatus.BAD_REQUEST)

        with session_scope():
            datastore.add_role_to_user(user, role)

    def delete_role_from_user(self, user_id, role_id):
        user = user_service.get_by_user_id(user_id)
        role = self.get_role_by_id(role_id)

        if not user:
            return error_response.fail("User with this id not found",
                                       status_code=HTTPStatus.BAD_REQUEST)

        if not role:
            return error_response.fail("Role with this id not found",
                                       status_code=HTTPStatus.BAD_REQUEST)

        if not user.has_role(role):
            return error_response.fail("User hasn't this role",
                                       status_code=HTTPStatus.BAD_REQUEST)

        with session_scope():
            datastore.remove_role_from_user(user, role)


role_service: RoleService = RoleService()
