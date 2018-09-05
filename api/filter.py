from typing import List
from decimal import Decimal
from .listings import Listing


def filter_results(offers: List[Listing], search_criteria: dict) -> set:
    selected = set()
    if search_criteria.get('star_rating'):
        selected.update([offer for offer in offers
                         if int(offer.starrating) >= search_criteria.get('star_rating')])
    if search_criteria.get('max_price'):
        selected.update([offer for offer in offers
                         if Decimal(offer.sellprice) <= search_criteria.get('max_price')])
    if search_criteria.get('min_price'):
        selected.update([offer for offer in offers
                         if Decimal(offer.sellprice) >= search_criteria.get('min_price')])
    if search_criteria.get('earliest_departure_time'):
        selected.update([offer for offer in offers
                         if offer.outbounddep >= search_criteria.get('earliest_departure_time')])
    if search_criteria.get('earliest_return_time'):
        selected.update([offer for offer in offers
                         if offer.inbounddep >= search_criteria.get('earliest_return_time')])
    return selected

