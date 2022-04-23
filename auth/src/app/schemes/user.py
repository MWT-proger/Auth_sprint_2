from models import User
from config import ma


class UserRegisterSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        fields = ("login", "email", "_password")


class UserLoginSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        fields = ("login", "_password")
