""" XMLParser """
# pylint: disable=too-few-public-methods

import re
import urllib
from typing import List, NamedTuple
from datetime import date
from xml.parsers.expat import ExpatError
import requests
import xmltodict
from config.settings import get_config
from utils.logger import logger
from .listings import Listing

API_URL = get_config('api_endpoint')
DATE_FORMAT = get_config('date_format')


class Params(NamedTuple):
    countryid: int
    page: str
    platform: str
    depart: str
    regionid: int
    areaid: int
    resortid: int
    depdate: str
    flex: int
    adults: int
    children: int
    duration: int


class XmlParser(object):
    """ Basic xml parser for retrieving data from the upstream API """

    @classmethod
    def get_listings(cls):
        query = Params(
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
        response = cls._retrieve_listings(query)
        return cls._parse_response(response.text)

    @staticmethod
    def _retrieve_listings(query_params: Params)-> str:
        try:
            query_params = query_params._asdict()
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
    def _parse_response(response: str)-> List[Listing]:
        try:
            # NOTE: we are getting some chars we cannot parse with xmltodict, so getting rid of them
            listings_cleaned = re.sub(r"\\r\\n|\\", '', response[1:-1])
            listings = xmltodict.parse(listings_cleaned)['Container']['Results']['Offer']
        except (ExpatError, TypeError) as e:
            logger.error(e)
            raise ValueError
        else:
            parsed_offers = []
            if listings:
                for listing in listings:
                    try:
                        parsed_offers.append(
                            Listing(
                                **{k.strip('@').lower(): urllib.parse.unquote_plus(v)
                                   for k, v in listing.items()}))
                    except TypeError as e:
                        logger.error(f"Missing field or wrong name. {e}")
            return parsed_offers

