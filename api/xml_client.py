import re
import urllib
import requests
import xmltodict
from datetime import date
from config.settings import get_config
from collections import namedtuple
from utils.logger import logger
from xml.parsers.expat import ExpatError
from .listings import Listing

API_URL = get_config('api_endpoint')
DATE_FORMAT = get_config('date_format')

params = namedtuple('params', [
    'countryid',
    'page',
    'platform',
    'depart',
    'regionid',
    'areaid',
    'resortid',
    'depdate',
    'flex',
    'adults',
    'children',
    'duration',
])


class XmlClient(object):
    """ Basic xml client for retrieving data from the upstream API """

    @classmethod
    def get_listings(cls):
        response = cls._retrieve_listings(
            countryid=1,
            page='SEARCH',
            platform='WEB',
            depart="|".join(['LGW', 'STN', 'LHR', 'LCY', 'SEN', 'LTN']),
            regionid=4,
            areaid=9,
            resortid=0,
            depdate=date(2018, 8, 15).strftime(DATE_FORMAT),
            flex=0,
            adults=2,
            children=0,
            duration=7,
        )
        return cls._parse_response(response)

    @staticmethod
    def _retrieve_listings(**kw):
        try:
            query_params = params(**kw)._asdict()
        except TypeError as e:
            logger.error(f"Missing param or wrong name. {e}")
        else:
            response = requests.get(API_URL, query_params)

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logger.error(e)
            else:
                return response

    @staticmethod
    def _parse_response(response):
        try:
            # NOTE: we are getting some chars we cannot parse with xmltodict, so getting rid of them
            listings_cleaned = re.sub(r"\\r\\n|\\", '', response.text[1:-1])
            offers = xmltodict.parse(listings_cleaned)['Container']['Results']['Offer']
        except (ExpatError, TypeError) as e:
            logger.error(e)
        else:
            parsed_offers = []
            if len(offers) > 0:
                for offer in offers:
                    try:
                        parsed_offers.append(
                            Listing(
                                **{k.strip('@').lower(): urllib.parse.unquote_plus(v)
                                   for k, v in offer.items()}))
                    except TypeError as e:
                        logger.error(f"Missing field or wrong name. {e}")
            return parsed_offers

