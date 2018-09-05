import pytest
from api.xml_parser import XmlParser, Params


def test_xmlparser():
    query_params = Params(
        countryid=1,
        page='SEARCH',
        platform='WEB',
        depart="|".join(['LGW', 'STN', 'LHR', 'LCY', 'SEN', 'LTN']),
        regionid=4,
        areaid=9,
        resortid=0,
        depdate='15/8/2018',
        flex=0,
        adults=2,
        children=0,
        duration=7,
    )
    response = XmlParser._retrieve_listings(query_params)
    assert response.status_code == 200


def test_xmlparser_bad_params():
    query_params = Params(
        countryid=None,
        page=None,
        platform=None,
        depart=None,
        regionid=None,
        areaid=None,
        resortid=None,
        depdate=None,
        flex=None,
        adults=None,
        children=None,
        duration=None,
    )
    response = XmlParser._retrieve_listings(query_params)
    assert response.status_code == 200


def test_xmlparser_parse_response():
    query_params = Params(
        countryid=1,
        page='SEARCH',
        platform='WEB',
        depart="|".join(['LGW', 'STN', 'LHR', 'LCY', 'SEN', 'LTN']),
        regionid=4,
        areaid=9,
        resortid=0,
        depdate='15/8/2018',
        flex=0,
        adults=2,
        children=0,
        duration=7,
    )
    response = XmlParser._retrieve_listings(query_params)
    parsed = XmlParser._parse_response(response.text)
    assert parsed


def test_xmlparser_not_valid_response():
    with pytest.raises(ValueError):
        XmlParser._parse_response('foo bar car')
