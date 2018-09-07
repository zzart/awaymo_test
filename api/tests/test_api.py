# pylint: disable=missing-docstring, invalid-name


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
    assert result.json


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


def test_check_malformatted_times(client, search_url):
    result = client.simulate_get(search_url, params={
        'earliest_departure_time': 'foo',
        'earliest_return_time': 'bar',
    })
    assert result.status_code == 400


def test_check_malformatted_numbers(client, search_url):
    result = client.simulate_get(search_url, params={
        'star_rating': 'foo',
    })
    assert result.status_code == 400


def test_check_malformatted_decimals(client, search_url):
    result = client.simulate_get(search_url, params={
        'max_price': 'foo',
    })
    assert result.status_code == 400


def test_check_only_get_is_working(client, search_url):
    result = client.simulate_post(search_url)
    assert result.status_code == 405
    result = client.simulate_put(search_url)
    assert result.status_code == 405
    result = client.simulate_delete(search_url)
    assert result.status_code == 405
    result = client.simulate_head(search_url)
    assert result.status_code == 405
    result = client.simulate_patch(search_url)
    assert result.status_code == 405
