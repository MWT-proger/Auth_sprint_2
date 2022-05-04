from http import HTTPStatus

import pytest
from functional.config import TestFilesPath, TestUrls
from functional.utils import app_logger, get_data
from functional.testdata import role_data

urls = TestUrls()
test_data = TestFilesPath()
logger = app_logger.get_logger("Test Role")


@pytest.mark.asyncio
async def test_get_all_roles(make_get_request, data_to_pg):
    response = await make_get_request(urls.get_all_roles)

    assert response.body == {"data": role_data.roles}
    assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_user_role(make_get_request, get_access):
    response = await make_get_request(urls.get_user_role + f"/{role_data.user.get('id')}", headers={
        "Authorization": f"Bearer {get_access}"})

    assert response.status == HTTPStatus.OK
    assert response.body == {"roles": [role_data.roles[1]]}


@pytest.mark.asyncio
async def test_add_and_delete_role(make_post_request, make_delete_request, get_access):
    response = await make_post_request(urls.add_new_role, data={"name": "test"})

    assert response.status == HTTPStatus.OK

    response = await make_delete_request(urls.delete_role + f"/{response.body['role_id']}",
                                         headers={"Authorization": f"Bearer {get_access}"})

    assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_add_role_to_user(make_post_request, get_access):
    response = await make_post_request(
        urls.add_role_to_user + f"/{role_data.user.get('id')}/{role_data.roles[0].get('id')}",
        headers={"Authorization": f"Bearer {get_access}"})

    assert response.status == HTTPStatus.OK
    assert response.body == {"message": "Role added successfully"}


@pytest.mark.asyncio
async def test_add_role_to_user_error(make_post_request, get_access):
    response = await make_post_request(
        urls.add_role_to_user + f"/{role_data.user.get('id')}/{role_data.roles[0].get('id')}",
        headers={"Authorization": f"Bearer {get_access}"})

    assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.body == {"data": "User already has this role",
                             "msg": "Something went wrong",
                             "status": "error"}


@pytest.mark.asyncio
async def test_delete_role_to_user(make_delete_request, get_access):
    response = await make_delete_request(
        urls.add_role_to_user + f"/{role_data.user.get('id')}/{role_data.roles[0].get('id')}",
        headers={"Authorization": f"Bearer {get_access}"})

    assert response.status == HTTPStatus.OK
    assert response.body == {"message": "Role deleted successfully"}


@pytest.mark.asyncio
async def test_delete_role_to_user_error(make_delete_request, get_access):
    response = await make_delete_request(
        urls.add_role_to_user + f"/{role_data.user.get('id')}/{role_data.roles[0].get('id')}",
        headers={"Authorization": f"Bearer {get_access}"})

    assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.body == {"data": "User hasn't this role",
                             "msg": "Something went wrong",
                             "status": "error"}


@pytest.mark.asyncio
async def test_delete_not_found_user(make_delete_request, get_access):
    response = await make_delete_request(
        urls.add_role_to_user + f"/{role_data.error_user_id}/{role_data.roles[0].get('id')}",
        headers={"Authorization": f"Bearer {get_access}"})

    assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.body == {"data": "User with this id not found",
                             "msg": "Something went wrong",
                             "status": "error"}


@pytest.mark.asyncio
async def test_delete_not_found_role(make_delete_request, get_access):
    response = await make_delete_request(
        urls.add_role_to_user + f"/{role_data.user.get('id')}/{role_data.error_role_id}",
        headers={"Authorization": f"Bearer {get_access}"})

    assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.body == {"data": "Role with this id not found",
                             "msg": "Something went wrong",
                             "status": "error"}
