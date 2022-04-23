from flask import Flask
from flask_marshmallow import Marshmallow

ma = Marshmallow()


def init_ma(app: Flask):
    ma.init_app(app)
