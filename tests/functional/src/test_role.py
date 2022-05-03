from http import HTTPStatus

import pytest
from functional.config import TestFilesPath, TestUrls
from functional.models import Role
from functional.utils import app_logger, get_data

urls = TestUrls()
test_data = TestFilesPath()
logger = app_logger.get_logger("Test Role")


@pytest.mark.asyncio
async def test_get_all_roles(make_get_request, data_to_pg):
    response = await make_get_request(urls.get_all_roles)

    assert response.body == {"data": [{
        "id": "6d12302c-6e39-4b83-aa94-c21de1a76e0e",
        "name": "user",
        "description": "description",
    },
        {
            "id": "6d12302c-6e39-4b83-aa94-c21de1a76e0a",
            "name": "admin",
            "description": "description",
        }]}
    assert response.status == HTTPStatus.OK


@pytest.mark.asyncio
async def test_get_user_role(make_get_request, get_access):
    response = await make_get_request(urls.get_user_role + "/cd547e34-c0da-41e0-be70-898d7e0cd17b", headers={
        "Authorization": f"Bearer {get_access}"})

    assert response.status == HTTPStatus.OK
    assert response.body == {"roles": [{
        "description": "description",
        "id": "6d12302c-6e39-4b83-aa94-c21de1a76e0a",
        "name": "admin"
    }]}


@pytest.mark.asyncio
async def test_add_and_delete_role(make_post_request, make_delete_request, get_access):
    response = await make_post_request(urls.add_new_role, data={"name": "test"})

    assert response.status == HTTPStatus.OK

    response = await make_delete_request(urls.delete_role + f"/{response.body['role_id']}",
                                         headers={"Authorization": f"Bearer {get_access}"})

    assert response.status == HTTPStatus.OK
