import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_app():
    test_client = TestClient(app)
    yield test_client  # testing happens here
