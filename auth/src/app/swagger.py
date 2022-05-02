from flasgger import Swagger
from flask import Flask

template = {
  "swagger": "2.0",
  "info": {
    "title": "Сервис авторизации",
    "description": "Разработан в целях обучения на Яндекс Практикуме",
    "version": "0.1.0",
    "contact": {
      "name": "Онлайн Кинотеатр",
      "url": "http://localhost:5000",
    }
  },
  "securityDefinitions": {
    "Bearer": {
      "type": "apiKey",
      "name": "Authorization",
      "in": "header",
      "description": "Авторизация JWT с использованием схемы Bearer. Пример: \"Authorization: Bearer {token}\""
    }
  }

}
swagger = Swagger(template=template)


def init_swagger(app: Flask):
    app.config['SWAGGER'] = {
        'title': 'Auth API',
        'uiversion': 3,
        "specs_route": "/swagger/"
    }
    swagger.init_app(app)
