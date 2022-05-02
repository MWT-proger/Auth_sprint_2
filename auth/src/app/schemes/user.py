from ma import ma
from marshmallow import fields
from models import User


class UserRegisterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("login", "email", "_password")


class UserUpdateSchema(ma.SQLAlchemyAutoSchema):
    login = fields.Str(required=False)
    email = fields.Email(required=False)
    _password = fields.Str(required=False)

    class Meta:
        model = User
        fields = ("login", "email", "_password")


class UserLoginSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ("login", "_password")
