from typing import List
from decimal import Decimal
from utils.logger import logger
from .listings import Listing


def get_results(offers: List[Listing], search_criteria: dict)-> list:

    if len(search_criteria) == 0:
        logger.error('Value search_criteria empty')
        raise ValueError('Please supply at least one search criteria')

    def filter_result(offer: Listing) -> bool:
        """ Determine if a single offer matches all search criteria """
        match = []
        if search_criteria.get('star_rating'):
            match.append(int(offer.starrating) >= search_criteria.get('star_rating'))
        if search_criteria.get('max_price'):
            match.append(Decimal(offer.sellprice) <= search_criteria.get('max_price'))
        if search_criteria.get('min_price'):
            match.append(Decimal(offer.sellprice) >= search_criteria.get('min_price'))
        if search_criteria.get('earliest_departure_time'):
            match.append(offer.outbounddep >= search_criteria.get('earliest_departure_time'))
        if search_criteria.get('earliest_return_time'):
            match.append(offer.inbounddep >= search_criteria.get('earliest_return_time'))
        return all(match)

    results = []
    for single_offer in offers:
        if filter_result(single_offer):
            results.append(single_offer)
    return results
