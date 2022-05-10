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

    class Meta:
        model = User
        fields = ("login", "email")


class UserChangePasswordSchema(ma.SQLAlchemyAutoSchema):
    _password = fields.Str(required=True)
    old_password = fields.Str(required=True)

    class Meta:
        model = User
        fields = ("old_password", "_password")


class UserLoginSchema(ma.SQLAlchemyAutoSchema):
    code_2fa = fields.Str(required=False)

    class Meta:
        model = User
        fields = ("login", "_password", "code_2fa")

