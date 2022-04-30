from database import session_scope
from datastore import datastore
from models import Role


class RoleService:
    def __init__(self):
        self.model = Role

    def create(self, name, description):
        with session_scope() as session:
            role = datastore.create_role(name=name, description=description)
            session.add(role)

    def get_all(self):
        return [role.serialize() for role in self.model.query.all()]

    def delete_by_id(self, id):
        with session_scope():
            self.model.query.filter_by(id=id).delete()


role_service: RoleService = RoleService()
