from ma import ma
from models import User


class UserRegisterSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        fields = ("login", "email", "_password")


class UserLoginSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        fields = ("login", "_password")
