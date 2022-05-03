from http import HTTPStatus

import pytest
from functional.config import TestFilesPath, TestUrls
from functional.models.auth import User
from functional.utils import app_logger, get_data

urls = TestUrls()
test_data = TestFilesPath()
logger = app_logger.get_logger("Test Account")


@pytest.mark.asyncio
async def test_registration(make_post_request):
    response = await make_post_request(urls.registration)

    assert response.status == HTTPStatus.BAD_REQUEST
