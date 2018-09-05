""" Main entry point of uwsgi routes """

import falcon
from falcondocs import FalconDocumentationResource, FalconDocumentationRouter
from api.resources import SearchResource, HealthResource

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
