from django.conf import settings
from django.utils.importlib import import_module

class AltoMiddleware(object):
    def process_request(self, request):
        # # Import the existing urlpatterns and add alto's patterns to it.
        # urlconf_module = import_module(settings.ROOT_URLCONF)
        # existing_urlpatterns = getattr(urlconf_module, 'urlpatterns')
        # urlpatterns = [url(r'^_alto/', include('alto.urls'))] + existing_urlpatterns
        # print request.urlconf
        request.urlconf = 'alto.utils.url_overrides'
