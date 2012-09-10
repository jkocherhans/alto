from django.conf import settings

class AltoMiddleware(object):
    def process_request(self, request):
        if settings.DEBUG:
            request.urlconf = 'alto.utils.url_overrides'
