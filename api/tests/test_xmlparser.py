# pylint: disable=duplicate-code, missing-docstring, protected-access, invalid-name
import pytest
from api.xml_parser import XmlParser


def test_xmlparser(query_params):
    response = XmlParser._retrieve_listings(query_params)
    assert response.status_code == 200


def test_xmlparser_parse_response(query_params):
    response = XmlParser._retrieve_listings(query_params)
    parsed = XmlParser._parse_response(response.text)
    assert parsed


def test_xmlparser_not_valid_response():
    with pytest.raises(ValueError):
        XmlParser._parse_response('foo bar car')
