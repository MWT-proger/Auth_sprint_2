from http import HTTPStatus

import pytest
from functional.config import TestFilesPath, TestUrls
from functional.utils import app_logger, get_data

urls = TestUrls()
test_data = TestFilesPath()
logger = app_logger.get_logger("Test Account")


@pytest.mark.asyncio
async def test_registration(make_post_request, role_reg_to_pg):
    test_data_1 = {

    }
    response = await make_post_request(urls.registration, data=test_data_1)

    assert response.status != HTTPStatus.OK
