from typing import NamedTuple, List
from decimal import Decimal
from utils.logger import logger
from utils.functions import get_time
from config.settings import get_config


class Listing(NamedTuple):
    """
    Simple listing structure.
    NOTE: Setting defaults to fields we don't operate on, just in case they don't get passed by upstream API.
    """
    sellprice: str
    starrating: str
    outbounddep: str
    inbounddep: str
    flightnetprice: str = None
    hotelnetprice: str = None
    brochurecode: str = None
    ourhtlid: str = None
    boardbasis: str = None
    roomtype: str = None
    resortname: str = None
    hotelname: str = None
    duration: str = None
    inboundfltnum: str = None
    inboundarr: str = None
    outboundfltnum: str = None
    outboundarr: str = None
    arraptname: str = None
    arraptcode: str = None
    depaptname: str = None
    depaptcode: str = None
    flightsuppler: str = None
    hotelsupplier: str = None
    type: str = None


def prepare_search_results(listings: List[Listing])-> str:
    result = {"summary": {}, "offers": []}

    if listings:
        for listing in listings:
            result['offers'].append(
             {"Sellprice": listing.sellprice,
              "Starrating": listing.starrating,
              "Hotelname": listing.hotelname,
              "Inboundfltnum": listing.inboundfltnum,
              "Outboundfltnum": listing.outboundfltnum,
              "Inboundarr": listing.inboundarr,
              "Inbounddep": listing.inbounddep}
            )
        result.update({
            "summary": {
                "most_expensive_price": max([Decimal(i.sellprice) for i in listings]),
                "cheapest_price": min([Decimal(i.sellprice) for i in listings]),
                "average_price": round(sum([Decimal(i.sellprice) for i in listings]) / len(listings), 2),
            }
        })
    return result


DATETIME_FORMAT = get_config('datetime_format')


def get_results(listings: List[Listing], search_criteria: dict)-> list:

    if len(search_criteria) == 0:
        logger.error('Value search_criteria empty')
        raise ValueError('Please supply at least one search criteria')

    def filter_result(listing: Listing) -> bool:
        """ Determine if a single offer matches all search criteria """
        match = []
        if search_criteria.get('star_rating'):
            match.append(int(listing.starrating) >= search_criteria.get('star_rating'))
        if search_criteria.get('max_price'):
            match.append(Decimal(listing.sellprice) <= search_criteria.get('max_price'))
        if search_criteria.get('min_price'):
            match.append(Decimal(listing.sellprice) >= search_criteria.get('min_price'))
        if search_criteria.get('earliest_departure_time'):
            match.append(get_time(listing.outbounddep, DATETIME_FORMAT) >= search_criteria.get('earliest_departure_time'))
        if search_criteria.get('earliest_return_time'):
            match.append(get_time(listing.inbounddep, DATETIME_FORMAT) >= search_criteria.get('earliest_return_time'))
        return all(match)

    results = []
    for single_listing in listings:
        if filter_result(single_listing):
            results.append(single_listing)
    return results
