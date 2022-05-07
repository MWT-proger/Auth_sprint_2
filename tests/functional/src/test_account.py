from http import HTTPStatus

import pytest
from functional.config import TestFilesPath, TestUrls
from functional.models import Role, RolesUsers, User
from functional.testdata import data_account
from functional.utils import app_logger, get_data

urls = TestUrls()
test_data = TestFilesPath()
logger = app_logger.get_logger("Test Account")


@pytest.mark.asyncio
async def test_registration_ok(make_post_request, db_session, role_reg_to_pg):
    response = await make_post_request(urls.registration, data=data_account.test_registration_user)

    assert response.status == HTTPStatus.OK
    assert response.body == {"msg": "Registration Success"}

    user_db = db_session.query(User).filter_by(login=data_account.test_registration_user["login"]).first()
    assert user_db.email == data_account.test_registration_user["email"]

    roles_users_db = db_session.query(RolesUsers).filter_by(user_id=user_db.id).first()
    roles_db = db_session.query(Role).filter_by(id=roles_users_db.role_id).first()
    assert roles_db.name == data_account.roles[0]["name"]


@pytest.mark.asyncio
async def test_registration_error(make_post_request, db_session, role_reg_to_pg, account_user_to_pg):
    response = await make_post_request(urls.registration, data=data_account.test_registration_user_error)

    assert response.status == HTTPStatus.BAD_REQUEST
    assert response.body == {
        "data":
            {
                "email": "email already exists"
            }
        ,
        "status": "fail"
    }


@pytest.mark.asyncio
async def test_login_error_wrong(make_post_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):

    response = await make_post_request(urls.login, data=data_account.user_login_invalid)

    assert response.status == HTTPStatus.UNAUTHORIZED
    assert response.body == {'msg': 'Wrong login or password', 'status': 'error'}


@pytest.mark.asyncio
async def test_login_error_required_file(make_post_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login_error)

    assert response.status == HTTPStatus.BAD_REQUEST
    assert response.body["data"] == "{'_password': ['Missing data for required field.']}"


@pytest.mark.asyncio
async def test_login_ok(make_post_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)

    assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_protected(make_post_request, make_get_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]

    response = await make_get_request(urls.protected, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status == HTTPStatus.OK
    assert response.body["logged_in_as"] == data_account.users[0]["id"]


@pytest.mark.asyncio
async def test_refresh_ok_invalid(make_post_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    refresh_token = response.body["refresh_token"]
    access_token = response.body["access_token"]

    response = await make_post_request(urls.refresh, headers={"Authorization": f"Bearer {refresh_token}"})
    assert response.status == HTTPStatus.OK

    response = await make_post_request(urls.refresh, headers={"Authorization": f"Bearer {refresh_token}"})

    assert response.status == HTTPStatus.UNAUTHORIZED
    assert response.body["msg"] == "Token has been revoked"
    assert response.body["status"] == "error"

    response = await make_post_request(urls.refresh, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body["msg"] == "Only refresh tokens are allowed"


@pytest.mark.asyncio
async def test_refresh_no_access(make_post_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]

    response = await make_post_request(urls.refresh, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body["msg"] == "Only refresh tokens are allowed"


@pytest.mark.asyncio
async def test_get_user(make_post_request, make_get_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]

    response = await make_get_request(urls.users_my, headers={"Authorization": f"Bearer {access_token}"})

    assert response.body["login"] == data_account.users[0]["login"]
    assert response.body["email"] == data_account.users[0]["email"]


@pytest.mark.asyncio
async def test_put_user_invalid_login(make_post_request, make_put_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]

    response = await make_put_request(urls.users_my,
                                      headers={"Authorization": f"Bearer {access_token}"},
                                      data=data_account.user_update_invalid_login)

    assert response.status == HTTPStatus.BAD_REQUEST
    assert response.body["data"] == {'login': 'login already exists'}


@pytest.mark.asyncio
async def test_put_user_invalid_email(make_post_request, make_put_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]

    response = await make_put_request(urls.users_my,
                                      headers={"Authorization": f"Bearer {access_token}"},
                                      data=data_account.user_update_invalid_email)

    assert response.status == HTTPStatus.BAD_REQUEST
    assert response.body["data"] == {'email': 'email already exists'}


@pytest.mark.asyncio
async def test_put_user_ok(make_post_request, make_put_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]

    response = await make_put_request(urls.users_my,
                                      headers={"Authorization": f"Bearer {access_token}"},
                                      data=data_account.user_update_ok)

    assert response.status == HTTPStatus.OK
    assert response.body["login"] == data_account.user_update_ok["login"]
    assert response.body["email"] == data_account.user_update_ok["email"]


@pytest.mark.asyncio
async def test_change_password_user_invalid(make_post_request, make_put_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]

    response = await make_put_request(urls.change_password, headers={"Authorization": f"Bearer {access_token}"},
                                      data=data_account.user_change_password_invalid)

    assert response.status == HTTPStatus.BAD_REQUEST
    assert response.body["data"] == {"old_password": "Old password is incorrect"}


@pytest.mark.asyncio
async def test_change_password_user_ok(make_post_request, make_put_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]

    response = await make_put_request(urls.change_password, headers={"Authorization": f"Bearer {access_token}"},
                                      data=data_account.user_change_password_ok)

    assert response.status == HTTPStatus.OK
    assert response.body == {"msg": "Password successfully changed"}
    response = await make_post_request(urls.login, data=data_account.user_login)
    assert response.status == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_login_history(make_post_request, make_get_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]

    response = await make_get_request(urls.my_login_history, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status == HTTPStatus.OK
    assert len(response.body) == 1


@pytest.mark.asyncio
async def test_logout_invalid(make_post_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.logout, headers={"Authorization": f"Bearer {data_account.invalid_refresh}"})

    assert response.status == HTTPStatus.UNAUTHORIZED
    assert response.body == {"msg": "Token has expired"}


@pytest.mark.asyncio
async def test_logout_ok(make_post_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]

    response = await make_post_request(urls.logout, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status == HTTPStatus.OK
    assert response.body == {"msg": "Success logout."}


@pytest.mark.asyncio
async def test_full_logout_invalid(make_post_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):

    response = await make_post_request(urls.full_logout,
                                       headers={"Authorization": f"Bearer {data_account.invalid_refresh}"})

    assert response.status == HTTPStatus.UNAUTHORIZED
    assert response.body == {"msg": "Token has expired"}


@pytest.mark.asyncio
async def test_full_logout_ok(make_post_request, db_session, role_reg_to_pg, account_user_to_pg, delete_data_all):
    """Проверка выхода со всех устройств"""
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token = response.body["access_token"]
    response = await make_post_request(urls.login, data=data_account.user_login)
    access_token_other = response.body["access_token"]

    response = await make_post_request(urls.full_logout, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status == HTTPStatus.OK
    assert response.body == {"msg": "Success logout."}

    response = await make_post_request(urls.full_logout, headers={"Authorization": f"Bearer {access_token_other}"})
    assert response.status == HTTPStatus.UNAUTHORIZED
    assert response.body == {"msg": "Token has been revoked"}

    response = await make_post_request(urls.full_logout, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status == HTTPStatus.UNAUTHORIZED
    assert response.body == {"msg": "Token has been revoked"}
