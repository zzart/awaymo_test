from falcon import testing
import pytest

from api.rest import api


@pytest.fixture()
def client():
    return testing.TestClient(api)


@pytest.fixture()
def search_url():
    return '/v1/search'


def test_health(client):
    doc = {'status': 'ok'}
    result = client.simulate_get('/v1/health')
    assert result.json == doc


def test_search_no_params(client, search_url):
    doc = {'title': 'Please supply at least one search criteria.'}
    result = client.simulate_get(search_url)
    assert result.status_code == 400
    assert result.json == doc


def test_search_single_param(client, search_url):
    result = client.simulate_get(search_url, params={'star_rating': 1})
    assert result.status_code == 200
    assert len(result.json) > 0


def test_search_no_results(client, search_url):
    doc = {'offers': [], 'summary': {}}
    result = client.simulate_get(search_url, params={'star_rating': 10})
    assert result.status_code == 200
    assert result.json == doc


def test_search_fake_params(client, search_url):
    result = client.simulate_get(search_url, params={'foo_bar': 10})
    assert result.status_code == 400


def test_search_multiple_params(client, search_url):
    result = client.simulate_get(search_url, params={
        'star_rating': 1,
        'earliest_departure_time': '10:00',
        'earliest_return_time': '12:00',
    })
    assert result.status_code == 200

