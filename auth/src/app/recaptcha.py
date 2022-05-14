from flask import Flask


# TODO # secret вынести в ключи
def init_recaptcha(app: Flask):
    app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdHJOkfAAAAAGPgNmHiq8f8zGNgPUhI29SEolpc'
    app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdHJOkfAAAAAJGWdXL45R5bTpDy0g82p7WLSVy_'