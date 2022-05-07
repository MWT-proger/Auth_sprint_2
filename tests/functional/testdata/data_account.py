users = [
    {
        "id": "6d12302c-7e39-4b83-aa94-c21de1a64e0e",
        "login": "account_user",
        "email": "account_user@mail.ru",
        "_password": "pbkdf2:sha256:260000$LILRuUM1GSreoWx7$549f77b5d7045d6689f7a8bb2111fb840f51db68aa1569b7b44032f0e262abce"
    },
    {
        "id": "7d12302c-8e39-4b83-aa95-c21de1a64e0e",
        "login": "account_user_2",
        "email": "account_user_2@mail.ru",
        "_password": "pbkdf2:sha256:260000$LILRuUM1GSreoWx7$549f77b5d7045d6689f7a8bb2111fb840f51db68aa1569b7b44032f0e262abce"
    }
]
user_login = {
        "login": "account_user",
        "_password": "12345"
    }
user_update_invalid_login = {
        "login": "account_user_2"
    }
user_update_invalid_email = {
        "email": "account_user_2@mail.ru"
    }
user_update_ok = {
        "login": "account_user_3",
        "email": "account_user_3@mail.ru"
    }


user_change_password_invalid = {
        "old_password": "invalid_password",
        "_password": "new_password"
    }
user_change_password_ok = {
        "old_password": "12345",
        "_password": "new_password"
    }
user_login_new = {
        "login": "account_user",
        "_password": "new_password"
    }


user_login_error = {
        "login": "account_user"
    }
user_login_invalid = {
        "login": "account_user",
        "_password": "54321"
    }

test_registration_user = {
        "login": "test_registration",
        "email": "test_registration@mail.ru",
        "_password": "test_registration"
    }
test_registration_user_error = {
        "login": "test_registration",
        "email": "account_user@mail.ru",
        "_password": "test_registration"
    }
roles = [
    {
        "id": "6d12302c-6e39-4b83-aa94-c21de1a76e0e",
        "name": "user",
        "description": "description"
    },
    {
        "id": "6d12302c-6e39-4b83-aa94-c21de1a76e0b",
        "name": "admin",
        "description": "description"
    }
]

invalid_refresh = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MTUxMTEwOCwianRpIjoiNzE0OWE1OTgtODYzNS00YTdkLTg0MjAtYWUxOTAwYThkYTZiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjZkMTIzMDJjLTZlMzktNGI4My1hYTk0LWMyMWRlMWE3NmUwZSIsIm5iZiI6MTY1MTUxMTEwOCwiZXhwIjoxNjUxNTExNDA4fQ.5HFvCozvF2un_S4goRIUSx8b8P12uIW6sDvKsCK-iRY"
