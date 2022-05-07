from api.v1.response_code import ResponseErrorApi
from flask import request
from flask.views import MethodView
from marshmallow.exceptions import ValidationError


class BaseAPI(MethodView, ResponseErrorApi):
    schema = None
    service = None

    def data_validation(self, data):
        try:
            self.schema.load(data)
            return True
        except ValidationError as e:
            self.error_400(str(e))

    def get_data(self):
        data = request.json
        return data

    def service_work(self, data):
        pass

    def post(self):
        data = self.get_data()
        if self.data_validation(data):
            return self.service_work(data)
