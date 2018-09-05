from typing import NamedTuple, List
from decimal import Decimal


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
