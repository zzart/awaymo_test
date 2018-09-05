""" Main entry point of uwsgi routes """

from decimal import Decimal
import simplejson
import falcon
from falcon.status_codes import HTTP_200, HTTP_400
from falcon.http_error import HTTPError
from falcondocs import FalconDocumentationResource, FalconDocumentationRouter
from utils.functions import JSONhandler, get_time
from utils.logger import logger
from config.settings import get_config
from .xml_parser import XmlParser
from .listings import prepare_search_results, get_results

TIME_FORMAT = get_config('time_format')


def check_times(req, resp, params):
    """
    Checks for well-formatted dates.
    :param req: request object
    :param resp: response object
    :param params: dict of query params
    :return: HTTP Error **400** or pass through upon successful validation
    """
    try:
        if req.get_param('earliest_departure_time'):
            get_time(req.get_param('earliest_departure_time'), TIME_FORMAT)
        if req.get_param('earliest_return_time'):
            get_time(req.get_param('earliest_return_time'), TIME_FORMAT)
    except ValueError as e:
        logger.error(e)
        raise HTTPError(HTTP_400, "One of the time params could not be parsed.")


class SearchResource(object):
    """ Search for offers matching search criteria """

    @falcon.before(check_times)
    def on_get(self, req, resp, **params):
        """
        :param req: request object
        :param resp: response object
        :param params: additional params passed upon request
        :returns: 200 with json obj or 400
        """

        try:
            args = {
                'earliest_departure_time': get_time(req.get_param('earliest_departure_time'), TIME_FORMAT)
                if req.get_param('earliest_departure_time') else None,
                'earliest_return_time': get_time(req.get_param('earliest_return_time'), TIME_FORMAT)
                if req.get_param('earliest_return_time') else None,
                'max_price': Decimal(req.get_param('max_price')) if req.get_param('max_price') else None,
                'min_price': Decimal(req.get_param('min_price')) if req.get_param('min_price') else None,
                'star_rating': req.get_param_as_int('star_rating') or None,
            }
            # get rid of empty keys
            args = {k: v for k, v in args.items() if v}
            if not args:
                raise HTTPError(HTTP_400, 'Please supply at least one search criteria.')

        except ValueError as e:
            logger.info(e)
            resp.status = HTTP_400
        else:
            search_results = get_results(listings=XmlParser.get_listings(), search_criteria=args)
            resp.body = simplejson.dumps(prepare_search_results(search_results), indent=2, default=JSONhandler)
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

# ROUTES ----------------------------------------------------------------------------------------------------------

search_resource = SearchResource()
api.add_route(api_ver + '/search', search_resource)

health_resource = HealthResource()
api.add_route(api_ver + '/health', health_resource)

FalconDocumentationResource(api).register(api_ver + '/docs')
