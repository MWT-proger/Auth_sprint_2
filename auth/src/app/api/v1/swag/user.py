signup_swagger = \
    {
        "tags": [
            "Signup API"
        ],
        "summary": "Регистрация пользователя",
        "consumes": [
            "application/json"
        ],
        "parameters": [
            {
                "in": "body",
                "name": "user",
                "description": "Данные для регистрации пользователя",
                "schema": {
                    "$ref": "#/definitions/SignupUserScheme"
                }
            }
        ],
        "produces": [
            "application/json"
        ],
        "operationId": "SignupAPI",
        "responses": {
            "200": {
                "description": "OK",
                "examples": {
                    "application/json": {
                        "msg": "Registration Success",
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
                "description": "Bad Request",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "data": [{"email": "email already exists"}]
                    }

                }
            }
        },
        "definitions": {
            "SignupUserScheme": {
                "type": "object",
                "required": [
                    "login",
                    "_password",
                    "email"
                ],
                "properties": {
                    "login": {
                        "type": "string",
                        "default": "login"
                    },
                    "_password": {
                        "type": "string",
                        "default": "password"
                    },
                    "email": {
                        "type": "string",
                        "default": "email"
                    }
                }
            }
        }
    }

user_me_swagger = \
    {
        "tags": [
            "User Me API"
        ],
        "summary": "Информация пользователя",
        "security": [
            {
                "Bearer": []
            }
        ],

        "produces": [
            "application/json"
        ],
        "operationId": "UserMeAPI",
        "responses": {
            "200": {
                "description": "OK",
                "schema": {
                    "$ref": "#/definitions/UserScheme"
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
            },
        },
        "definitions": {
            "UserScheme": {
                "type": "object",
                "required": [
                    "login",
                    "email"
                ],
                "properties": {
                    "login": {
                        "type": "string",
                        "default": "login"
                    },
                    "email": {
                        "type": "string",
                        "default": "email"
                    }
                }
            }
        }
    }
update_user_swagger = \
    {
        "tags": [
            "Update User API"
        ],
        "summary": "Изменение данных пользователя",
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
                "name": "user",
                "description": "Данные для редактирования пользователя",
                "schema": {
                    "$ref": "#/definitions/UpdateUserScheme"
                }
            }
        ],
        "produces": [
            "application/json"
        ],
        "operationId": "UpdateUserAPI",
        "responses": {
            "200": {
                "description": "OK",
                "schema": {
                    "$ref": "#/definitions/UserScheme"
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
            "401": {
                "description": "UNAUTHORIZED",
                "examples": {
                    "application/json": {
                         "msg": "Token has been revoked",
                         "status": "error"
                    }
                }
            },
            "400": {
                "description": "Bad Request",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "data": [{"email": "email already exists"}]
                    }

                }
            }
        },
        "definitions": {
            "UpdateUserScheme": {
                "type": "object",
                "properties": {
                    "login": {
                        "type": "string",
                        "default": "login"
                    },
                    "_password": {
                        "type": "string",
                        "default": "password"
                    },
                    "old_password": {
                        "type": "string",
                        "default": "old_password"
                    },
                    "email": {
                        "type": "string",
                        "default": "email"
                    }
                }
            }
        }
    }

change_password_user_swagger = \
    {
        "tags": [
            "Change Password User API"
        ],
        "summary": "Смена пароль пользователя",
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
                "name": "user",
                "description": "Данные для смены пароля",
                "schema": {
                    "$ref": "#/definitions/UserChangePasswordSchema"
                }
            }
        ],
        "produces": [
            "application/json"
        ],
        "operationId": "UserChangePasswordAPI",
        "responses": {
            "200": {
                "description": "OK",
                "examples": {
                    "application/json": {
                        "msg": "Password successfully changed"
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
            "401": {
                "description": "UNAUTHORIZED",
                "examples": {
                    "application/json": {
                         "msg": "Token has been revoked",
                         "status": "error"
                    }
                }
            },
            "400": {
                "description": "Bad Request",
                "examples": {
                    "application/json": {
                        "status": "fail",
                        "data": [{"old_password": "Old password is incorrect"}]
                    }

                }
            }
        },
        "definitions": {
            "UserChangePasswordSchema": {
                "type": "object",
                "required": [
                    "_password",
                    "old_password"
                ],
                "properties": {
                    "_password": {
                        "type": "string",
                        "default": "password"
                    },
                    "old_password": {
                        "type": "string",
                        "default": "old_password"
                    }
                }
            }
        }
    }

get_login_history_swagger = \
    {
        "tags": [
            "Login History API"
        ],
        "summary": "Вывод истории аунтификации пользователя",
        "security": [
            {
                "Bearer": []
            }
        ],
        "produces": [
            "application/json"
        ],
        "operationId": "LoginHistoryUserAPI",
        "responses": {
            "200": {
                "description": "OK",
                "type": "array",
                "schema": {
                    "$ref": "#/definitions/LoginHistoryUserScheme"
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
            "401": {
                "description": "UNAUTHORIZED",
                "examples": {
                    "application/json": {
                         "msg": "Token has been revoked",
                         "status": "error"
                    }
                }
            }
        },
        "definitions": {
            "LoginHistoryUserScheme": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "default": "1bfbe3f7-aa07-44d5-acfd-185568101b5f"
                    },
                    "datetime": {
                        "type": "string",
                        "default": "2022-05-02T13:37:03.143454"
                    },
                    "user_agent": {
                        "type": "string",
                        "default": "PostmanRuntime/7.29.0"
                    },
                    "ip": {
                        "type": "string",
                        "default": "127.0.0.1"
                    }
                }
            }
        }
    }

