# pylint: disable=missing-docstring, protected-access

from falcon import testing
import pytest
from api.rest import api
from api.xml_parser import XmlParser


@pytest.fixture()
def client():
    return testing.TestClient(api)


@pytest.fixture()
def search_url():
    return '/v1/search'


@pytest.fixture()
def query_params():
    return XmlParser._get_params()
