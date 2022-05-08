from config import get_config as config
from flask import Flask

# TODO # secret вынести в ключи
def init_oauth(app: Flask):
    app.config["OAUTH_CREDENTIALS"] = {
        'facebook': {
            'id': '470154729788964',
            'secret': '010cc08bd4f51e34f3f3e684fbdea8a7'
        },
        'twitter': {
            'id': '3RzWQclolxWZIMq5LJqzRZPTl',
            'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
        },
        'yandex': {
            'id': 'b8b6f61f1eb7404d8b2b61b5313b0877',
            'secret': '7ae44a90f91c41ab9c79e7a8794495cb'
        }
    }
