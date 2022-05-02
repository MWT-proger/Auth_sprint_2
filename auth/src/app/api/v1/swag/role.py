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
    "security": [
        {
            "Bearer": []
        }
    ],
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
        },
        {

            "in": "path",
            "name": "role_id",
            "schema": {
                "type": "uuid"

            },
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
                    "id": "some role id"
                }
            }
        },
        "400": {
            "description": "Bad Request",
            "examples": {
                "application/json": {
                    "status": "fail",
                    "data": [{"name": "Role with this name already exist"}]
                }

            }
        },
    },
    "definitions": {
        "UpdateRoleScheme": {
            "type": "object",
            "required": [
                "title",
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "default": "name"
                },
                "description": {
                    "type": "string",
                    "default": "description"
                }
            }
        }
    }
}

delete_role = {
    "tags": [
        "Role API"
    ],
    "summary": "Удаление роли",
    "security": [
        {
            "Bearer": []
        }
    ],
    "consumes": [
        "application/json"
    ],
    "parameters": [
        {
            "in": "path",
            "name": "role_id",
            "schema": {
                "type": "uuid"
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
                "application/json": {"message": "Роль успешно удалена"}
            }
        },
        "400": {
            "description": "Bad Request",
            "examples": {
                "application/json": {
                    "status": "fail",
                    "data": []
                }

            }
        },
        "500": {
            "description": "Internal Server Error",
            "examples": {
                "application/json": {
                    "msg": "Something went wrong",
                    "status": "error",
                    "data": []
                }

            }
        },
    },
    "definitions": {
        "UpdateRoleScheme": {
            "type": "object",
            "required": [
                "title",
            ],
            "properties": {
                "name": {
                    "type": "string",
                    "default": "name"
                },
                "description": {
                    "type": "string",
                    "default": "description"
                }
            }
        }
    }
}

add_role = {
    "tags": [
        "User Role API"
    ],
    "summary": "Добавление роли пользователю",
    "security": [
        {
            "Bearer": []
        }
    ],
    "consumes": [
        "application/json"
    ],
    "parameters": [
        {
            "in": "path",
            "name": "user_id",
            "schema": {
                "type": "uuid"
            }
        },
        {
            "in": "path",
            "name": "role_id",
            "schema": {
                "type": "uuid"
            }
        }
    ],
    "produces": [
        "application/json"
    ],
    "operationId": "UserRoleAPI",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {"message": "Role added successfully"}
            }
        },
        "400": {
            "description": "Bad Request",
            "examples": {
                "application/json": {
                    "status": "fail",
                    "data": []
                }

            }
        },
        "500": {
            "description": "Internal Server Error",
            "examples": {
                "application/json": {
                    "msg": "Something went wrong",
                    "status": "error",
                    "data": []
                }

            }
        },
    },
}

remove_role = {
    "tags": [
        "User Role API"
    ],
    "summary": "Удаление роли у пользователя",
    "security": [
        {
            "Bearer": []
        }
    ],
    "consumes": [
        "application/json"
    ],
    "parameters": [
        {
            "in": "path",
            "name": "user_id",
            "schema": {
                "type": "uuid"
            }
        },
        {
            "in": "path",
            "name": "role_id",
            "schema": {
                "type": "uuid"
            }
        }
    ],
    "produces": [
        "application/json"
    ],
    "operationId": "UserRoleAPI",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {"message": "Role deleted successfully"}
            }
        },
        "400": {
            "description": "Bad Request",
            "examples": {
                "application/json": {
                    "status": "fail",
                    "data": []
                }

            }
        },
        "500": {
            "description": "Internal Server Error",
            "examples": {
                "application/json": {
                    "msg": "Something went wrong",
                    "status": "error",
                    "data": []
                }

            }
        },
    },
}

get_user_role = {
    "tags": [
        "User Role API"
    ],
    "summary": "Получение роли пользователя",
    "security": [
        {
            "Bearer": []
        }
    ],
    "consumes": [
        "application/json"
    ],
    "parameters": [
        {
            "in": "path",
            "name": "user_id",
            "schema": {
                "type": "uuid"
            }
        }
    ],
    "produces": [
        "application/json"
    ],
    "operationId": "UserRoleAPI",
    "responses": {
        "200": {
            "description": "OK",
            "examples": {
                "application/json": {"roles": [{
                    "description": None,
                    "id": "uuid",
                    "name": "user"
                }]}
            }
        },
        "400": {
            "description": "Bad Request",
            "examples": {
                "application/json": {
                    "status": "fail",
                    "data": []
                }

            }
        },
        "500": {
            "description": "Internal Server Error",
            "examples": {
                "application/json": {
                    "msg": "Something went wrong",
                    "status": "error",
                    "data": []
                }

            }
        },
    },
}
