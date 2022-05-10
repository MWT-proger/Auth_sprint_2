from config import get_config as config
from flask import Flask

# TODO # secret вынести в ключи
def init_oauth(app: Flask):
    app.config["OAUTH_CREDENTIALS"] = {
        'yandex': {
            'id': 'b8b6f61f1eb7404d8b2b61b5313b0877',
            'secret': '7ae44a90f91c41ab9c79e7a8794495cb'
        },
        'mail': {
            'id': '8ec4255c412845c2b153d8692fdd08e8',
            'secret': 'a54cf88bbd3b48f7b0b621a96470c902',
        },
        'vk': {
            'id': '8162682',
            'secret': 'O50bUOEE9HPgNj6RrHpo',
        }
    }
