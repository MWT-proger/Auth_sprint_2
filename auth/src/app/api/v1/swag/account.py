login_swagger = \
    {
        "tags": [
            "Login API"
        ],
        "summary": "Аунтификация пользователя",
        "consumes": [
            "application/json"
        ],
        "parameters": [
            {
                "in": "body",
                "name": "user",
                "description": "Данные для аунтификации пользователя",
                "schema": {
                    "$ref": "#/definitions/LoginScheme"
                }
            }
        ],
        "produces": [
            "application/json"
        ],
        "operationId": "LoginAPI",
        "responses": {
            "200": {
                "description": "OK",
                "examples": {
                    "application/json": {
                        "access_token": "some access token",
                        "refresh_token": "some refresh token"
                    }
                }
            },
            "500": {
                "description": "Ошибка!"
            }
        },
        "definitions": {
            "LoginScheme": {
                "type": "object",
                "required": [
                    "login",
                    "_password"
                ],
                "properties": {
                    "login": {
                        "type": "string",
                        "default": "login"
                    },
                    "_password": {
                        "type": "string",
                        "default": "password"
                    }
                }
            }
        }
    }


error = {
    "status": "fail/error",
    "message": "some text",
    "data": [{"title": "A title is required"}]
}
