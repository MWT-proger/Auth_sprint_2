from marshmallow import fields

from ma import ma
from models import Role


class RoleCreateSchema(ma.SQLAlchemyAutoSchema):
    name = fields.Str(required=True)
    description = fields.Str(required=False)

    class Meta:
        model = Role
        fields = ("name", "description")


class RoleUpdateSchema(ma.SQLAlchemyAutoSchema):
    name = fields.Str(required=False)
    description = fields.Str(required=False)

    class Meta:
        model = Role
        fields = ("name", "description")
