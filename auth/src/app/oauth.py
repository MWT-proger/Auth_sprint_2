from config import get_config as config
from flask import Flask


# TODO # secret вынести в ключи
def init_oauth(app: Flask):
    app.config["OAUTH_CREDENTIALS"] = {
        'yandex': {
            'id': config.OAUTH.YANDEX_ID,
            'secret': config.OAUTH.YANDEX_SECRET
        },
        'mail': {
            'id': config.OAUTH.MAIL_ID,
            'secret': config.OAUTH.MAIL_SECRET,
        },
        'vk': {
            'id': config.OAUTH.VK_ID,
            'secret': config.OAUTH.VK_SECRET,
        }
    }
