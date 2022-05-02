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
            "401": {
                "description": "UNAUTHORIZED",
                "examples": {
                    "application/json": {
                         "msg": "Wrong login or password",
                         "status": "error"
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
            "400": {
                "description": "BAD REQUEST",
                "examples": {
                    "application/json": {
                        "msg": "The data is incorrect",
                        "status": "error",
                        "data": []
                    }

                }
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

refresh_token_swagger = \
    {
        "tags": [
            "Update JWT"
        ],
        "summary": "Обновление Access и Refresh токенов. Необходимо авторизовываться через refresh token",
        "security": [
            {
                "Bearer": []
            }
        ],
        "operationId": "RefreshTokenAPI",
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
            "401": {
                "description": "UNAUTHORIZED",
                "examples": {
                    "application/json": {
                         "msg": "Token has been revoked",
                         "status": "error"
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
            }
        }
    }


logout_swagger = \
    {
        "tags": [
            "Logout"
        ],
        "summary": "Выход пользователя",
        "security": [
            {
                "Bearer": []
            }
        ],
        "operationId": "LogoutUser",
        "responses": {
            "200": {
                "description": "OK",
                "examples": {
                    "application/json":
                        {"msg": "Success logout."}
                }
            },
            "401": {
                "description": "UNAUTHORIZED",
                "examples": {
                    "application/json": {
                         "msg": "Token has been revoked",
                         "status": "error"
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
            }
        }
    }


full_logout_swagger = \
    {
        "tags": [
            "Full logout"
        ],
        "summary": "Выход пользователя со всех устройств",
        "security": [
            {
                "Bearer": []
            }
        ],
        "operationId": "FullLogoutUser",
        "responses": {
            "200": {
                "description": "OK",
                "examples": {
                    "application/json":
                        {"msg": "Success logout."}
                }
            },
            "401": {
                "description": "UNAUTHORIZED",
                "examples": {
                    "application/json": {
                         "msg": "Token has been revoked",
                         "status": "error"
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
            }
        }
    }


protected_swagger = \
    {
        "tags": [
            "Protected"
        ],
        "summary": "Проверка авторизации",
        "security": [
            {
                "Bearer": []
            }
        ],
        "operationId": "ProtectedUser",
        "responses": {
            "200": {
                "description": "OK",
                "examples": {
                    "application/json":
                        {"logged_in_as": "6d12302c-6e39-4b83-aa94-c21de1a76e0e"}
                }
            },
            "401": {
                "description": "UNAUTHORIZED",
                "examples": {
                    "application/json": {
                         "msg": "Token has been revoked",
                         "status": "error"
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
            }
        }
    }
