from functional.models.new_base_model import NewBaseModel as BaseModel


class User(BaseModel):
    login: str
    email: str
    _password: str
