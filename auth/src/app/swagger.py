from flasgger import Swagger
from flask import Flask

swagger = Swagger()


def init_swagger(app: Flask):
    swagger.init_app(app)
