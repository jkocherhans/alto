from django.conf import settings
from django.conf.urls import url, include
from django.utils.importlib import import_module

# Import the existing urlpatterns and add alto's patterns to it.
urlconf_module = import_module(settings.ROOT_URLCONF)
existing_urlpatterns = getattr(urlconf_module, 'urlpatterns')
urlpatterns = [url(r'^_alto/', include('alto.urls'))] + existing_urlpatterns
