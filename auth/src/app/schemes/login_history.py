from ma import ma
from models import LoginHistory


class LoginHistorySchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = LoginHistory
        fields = ("id", "datetime", "user_agent", "ip")
