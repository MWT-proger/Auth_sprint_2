get_roles = \
    {
        "tags": [
            "Role API"
        ],
        "summary": "Получение всех ролей",
        "consumes": [
            "application/json"
        ],
        "operationId": "RoleAPI",
        "responses": {
            "200": {
                "description": "OK",
                "examples": {
                    "application/json": {
                        "data": [
                            {
                                "description": "string",
                                "id": "uuid",
                                "name": "string"
                            },
                        ]
                    }
                }
            },
            "500": {
                "description": "Ошибка!"
            }
        },
    }

update_role = {
    "tags": [
        "Role API"
    ],
    "summary": "Изменение роли",
    "consumes": [
        "application/json"
    ],
    "parameters": [
        {
            "in": "body",
            "name": "role",
            "description": "Данные для внесения изменений",
            "schema": {
                "$ref": "#/definitions/UpdateRoleScheme"
            }
        }
    ],
    "produces": [
        "application/json"
    ],
    "operationId": "RoleAPI",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {
                    "title": "string",
                    "": "some refresh token"
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
