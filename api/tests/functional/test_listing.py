# pylint: disable=missing-docstring, invalid-name,redefined-outer-name
import pytest
from api.listings import Listing, search_listings, prepare_search_results
from utils.functions import format_time
from config.settings import get_config

TIME_FORMAT = get_config('time_format')


@pytest.fixture()
def sample_data():
    return [
        Listing(
            sellprice='100',
            starrating='1',
            outbounddep='16/08/2018 06:25',
            inbounddep='16/08/2018 00:25',
        ),
        Listing(
            sellprice='200',
            starrating='2',
            outbounddep='16/08/2018 07:25',
            inbounddep='16/08/2018 10:25',
        ),
        Listing(
            sellprice='300',
            starrating='4',
            outbounddep='16/08/2018 08:25',
            inbounddep='16/08/2018 11:25',
        ),
        Listing(
            sellprice='400',
            starrating='4',
            outbounddep='16/08/2018 09:25',
            inbounddep='16/08/2018 12:25',
        ),
        Listing(
            sellprice='500',
            starrating='5',
            outbounddep='16/08/2018 10:25',
            inbounddep='16/08/2018 13:25',
        ),
        Listing(
            sellprice='600',
            starrating='6',
            outbounddep='16/08/2018 11:25',
            inbounddep='16/08/2018 20:25',
        ),
    ]


def test_filter_prices(sample_data):
    search_criteria = {
        'max_price': 600.00,
        'min_price': 100.00,
        'star_rating': None,
        'earliest_departure_time': None,
        'earliest_return_time': None,
    }
    result = search_listings(sample_data, search_criteria)
    assert len(result) == 6
    search_criteria = {
        'max_price': 100.00,
        'min_price': 100.00,
        'star_rating': None,
        'earliest_departure_time': None,
        'earliest_return_time': None,
    }
    result = search_listings(sample_data, search_criteria)
    assert len(result) == 1


def test_filter_prices_no_numbers(sample_data):
    search_criteria = {
        'max_price': 'foo',
        'min_price': 'bar',
        'star_rating': None,
        'earliest_departure_time': None,
        'earliest_return_time': None,
    }
    with pytest.raises(TypeError):
        search_listings(sample_data, search_criteria)


def test_star_rating(sample_data):
    search_criteria = {
        'max_price': None,
        'min_price': None,
        'star_rating': 1,
        'earliest_departure_time': None,
        'earliest_return_time': None,
    }
    result = search_listings(sample_data, search_criteria)
    assert len(result) == 6
    search_criteria = {
        'max_price': None,
        'min_price': None,
        'star_rating': 6,
        'earliest_departure_time': None,
        'earliest_return_time': None,
    }
    result = search_listings(sample_data, search_criteria)
    assert len(result) == 1


def test_star_rating_no_numbers(sample_data):
    search_criteria = {
        'max_price': None,
        'min_price': None,
        'star_rating': 'foo',
        'earliest_departure_time': None,
        'earliest_return_time': None,
    }
    with pytest.raises(TypeError):
        search_listings(sample_data, search_criteria)


def test_departure_time(sample_data):
    search_criteria = {
        'max_price': None,
        'min_price': None,
        'star_rating': None,
        'earliest_departure_time': format_time('10:00', TIME_FORMAT),
        'earliest_return_time': None,
    }
    result = search_listings(sample_data, search_criteria)
    assert len(result) == 2
    search_criteria = {
        'max_price': None,
        'min_price': None,
        'star_rating': 6,
        'earliest_departure_time': format_time('12:00', TIME_FORMAT),
        'earliest_return_time': None,
    }
    result = search_listings(sample_data, search_criteria)
    assert not result


def test_data_formatting(sample_data):
    results = prepare_search_results(sample_data)
    assert results
    assert isinstance(results, dict)
    assert 'summary' in results.keys()
    assert 'offers' in results.keys()

