from http import HTTPStatus

import pytest
from functional.config import TestFilesPath, TestUrls
from functional.models import Role
from functional.utils import app_logger, get_data

urls = TestUrls()
test_data = TestFilesPath()
logger = app_logger.get_logger("Test Role")


@pytest.mark.asyncio
async def test_get_all_roles(make_get_request, db_session, roles_to_pg):

    response = await make_get_request(urls.get_all_roles)

    assert response.body == []
    assert response.status == HTTPStatus.OK
