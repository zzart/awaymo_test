from falcon import testing
import pytest

from api.rest import api


@pytest.fixture()
def client():
    return testing.TestClient(api)


@pytest.fixture()
def search_url():
    return '/v1/search'
