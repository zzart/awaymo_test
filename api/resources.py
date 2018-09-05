from decimal import Decimal
import simplejson
from falcon.status_codes import HTTP_200, HTTP_400
from utils.functions import JSONhandler
from utils.logger import logger
from .filter import filter_results
from .xml_client import XmlClient


class SearchResource(object):
    """  """

    def on_get(self, req, resp):
        """
        :param req: request object
        :param resp: response object
        :returns: 200 with json obj or 400
        """

        try:
            args = {
                'earliest_departure_time': req.get_param('earliest_departure_time'),
                'earliest_return_time': req.get_param('earliest_return_time'),
                'max_price': Decimal(req.get_param('max_price', default=0)),
                'min_price': Decimal(req.get_param('min_price', default=0)),
                'star_rating': req.get_param_as_int('star_rating'),
            }

        except ValueError as e:
            logger.info(e)
            resp.status = HTTP_400
        else:
            search_results = filter_results(offers=XmlClient.get_listings(), search_criteria=args)
            resp.body = simplejson.dumps([result for result in search_results], indent=2, default=JSONhandler)
            resp.status = HTTP_200
