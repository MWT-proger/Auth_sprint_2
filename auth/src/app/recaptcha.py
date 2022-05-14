from config import get_config as config
from flask import Flask


# TODO # secret вынести в ключи
def init_recaptcha(app: Flask):
    app.config['RECAPTCHA_PUBLIC_KEY'] = config.RECAPTCHA.RECAPTCHA_PUBLIC_KEY
    app.config['RECAPTCHA_PRIVATE_KEY'] = config.RECAPTCHA.RECAPTCHA_PRIVATE_KEY
