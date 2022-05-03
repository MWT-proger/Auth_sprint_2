from http import HTTPStatus

import pytest
from functional.config import TestFilesPath, TestUrls
from functional.utils import app_logger, get_data
from functional.testdata import data_account
from functional.models import User, RolesUsers, Role

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
