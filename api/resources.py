from decimal import Decimal
import simplejson
from falcon.status_codes import HTTP_200, HTTP_400
from utils.functions import JSONhandler
from utils.logger import logger
from .filter import get_results
from .xml_client import XmlClient
from .listings import prepare_search_results


class SearchResource(object):
    """ Search for offers matching search criteria """

    def on_get(self, req, resp):
        """
        :param req: request object
        :param resp: response object
        :returns: 200 with json obj or 400
        """

        try:
            args = {
                'earliest_departure_time': req.get_param('earliest_departure_time') or None,
                'earliest_return_time': req.get_param('earliest_return_time') or None,
                'max_price': Decimal(req.get_param('max_price')) if req.get_param('max_price') else None,
                'min_price': Decimal(req.get_param('min_price')) if req.get_param('min_price') else None,
                'star_rating': req.get_param_as_int('star_rating') or None,
            }
            # get rid of empty keys
            args = {k: v for k, v in args.items() if v}

        except ValueError as e:
            logger.info(e)
            resp.status = HTTP_400
        else:
            search_results = get_results(offers=XmlClient.get_listings(), search_criteria=args)
            resp.body = simplejson.dumps(prepare_search_results(search_results), indent=2, default=JSONhandler)
            resp.status = HTTP_200


class HealthResource(object):
    """ Ping me to check if I'm alive """

    def on_get(self, req, resp):
        """
        :param req: request object
        :param resp: response object
        :returns: 200
        """
        resp.body = simplejson.dumps({'status': 'ok'})
        resp.status = HTTP_200
