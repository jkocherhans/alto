from django.conf import settings
from django.utils.importlib import import_module

class AltoMiddleware(object):
    def process_request(self, request):
        if settings.DEBUG:
            request.urlconf = 'alto.utils.url_overrides'
