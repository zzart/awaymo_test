""" Main entry point of uwsgi routes """
# pylint: disable=invalid-name,unused-argument,too-few-public-methods,no-self-use,bad-continuation

import decimal
from decimal import Decimal
import simplejson
import falcon
from falcon.status_codes import HTTP_200, HTTP_400
from falcon.http_error import HTTPError
from falcondocs import FalconDocumentationResource, FalconDocumentationRouter
from utils.functions import json_handler, format_time
from utils.logger import logger
from config.settings import get_config
from api.xml_parser import XmlParser
from api.listings import prepare_search_results, search_listings

TIME_FORMAT = get_config('time_format')


def check_types(req, resp, params):
    """
    Checks for well-formatted dates.
    :param req: request object
    :param resp: response object
    :param params: dict of query params
    :return: HTTP Error **400** or pass through upon successful validation
    """
    types = (
        ('earliest_departure_time', format_time),
        ('earliest_return_time', format_time),
        ('max_price', Decimal),
        ('min_price', Decimal),
        ('star_rating', int)
    )

    try:
        for item in types:
            if req.get_param(item[0]):
                item[1](req.get_param(item[0]))
    except (ValueError, decimal.InvalidOperation) as e:
        logger.error(e)
        raise HTTPError(HTTP_400, f"{item[0]} could not be parsed.")


class SearchResource(object):
    """ Search for offers matching search criteria """

    @falcon.before(check_types)
    def on_get(self, req, resp, **params):
        """
        :param req: request object
        :param resp: response object
        :param params: additional params passed upon request
        :returns: 200 with json obj or 400
        """

        args = {
            'earliest_departure_time': format_time(
                req.get_param('earliest_departure_time'), TIME_FORMAT)
            if req.get_param('earliest_departure_time') else None,
            'earliest_return_time': format_time(
                req.get_param('earliest_return_time'), TIME_FORMAT)
            if req.get_param('earliest_return_time') else None,
            'max_price': Decimal(req.get_param('max_price'))
            if req.get_param('max_price') else None,
            'min_price': Decimal(req.get_param('min_price'))
            if req.get_param('min_price') else None,
            'star_rating': req.get_param_as_int('star_rating') or None,
        }
        # get rid of empty keys
        args = {k: v for k, v in args.items() if v}
        if not args:
            raise HTTPError(HTTP_400, 'Please supply at least one search criteria.')

        search_results = search_listings(listings=XmlParser.get_listings(), search_criteria=args)
        resp.body = simplejson.dumps(
            prepare_search_results(search_results), indent=2, default=json_handler)
        resp.status = HTTP_200


class HealthResource(object):
    """ Ping me to check if I'm alive """

    def on_get(self, req, resp, *params):
        """
        :param req: request object
        :param resp: response object
        :param params: additional params passed upon request
        :returns: 200
        """
        resp.body = simplejson.dumps({'status': 'ok'})
        resp.status = HTTP_200


# falcon.API instances are callable WSGI apps
wsgi_app = api = falcon.API(
    router=FalconDocumentationRouter())

api_ver = '/v1'

# ROUTES ----------------------------------------------------

search_resource = SearchResource()
api.add_route(api_ver + '/search', search_resource)

health_resource = HealthResource()
api.add_route(api_ver + '/health', health_resource)

FalconDocumentationResource(api).register(api_ver + '/docs')
