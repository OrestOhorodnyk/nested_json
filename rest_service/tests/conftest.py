import base64

import pytest

from app import create_app


@pytest.fixture(scope='session')
def client():
    app = create_app()
    with app.app.test_client() as c:
        yield c


@pytest.fixture(scope='session')
def invalid_credentials():
    return base64.b64encode(b'testuser:testpassword').decode('utf-8')


@pytest.fixture(scope='session')
def valid_credentials():
    return base64.b64encode(b'admin:admin').decode('utf-8')
