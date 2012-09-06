import json
import os
from django import http
from django.conf import settings
from django.template import RequestContext
from django.template.loaders.filesystem import Loader
from alto import urlviz
from alto.templates import find_template, find_templates

ALTO_TEMPLATE_DIRS = [os.path.join(os.path.dirname(__file__), 'templates')]

def index(request, mode=None):
    # Use the filesystem loader directly here so we don't need to require
    # people to add the app_directories template loader if they don't want to.
    loader = Loader()
    template, name = loader('alto/index.html', template_dirs=ALTO_TEMPLATE_DIRS)
    context = RequestContext(request, {
        'url_scheme': getattr(settings, 'ALTO_URL_SCHEME', 'mvim'),
        'query': request.GET.get('q', ''),
        'mode': mode or '',
        'STATIC_URL': '/_alto/media/',
    })
    return http.HttpResponse(template.render(context))

def url_patterns(request):
    patterns = urlviz.inspect_urlpatterns()
    return http.HttpResponse(json.dumps(patterns, sort_keys=True, indent=2))

def view_detail(request, module_path, view_name):
    view = urlviz.load_view(module_path, view_name)
    view, decorators = urlviz.extract_view(view)
    data = urlviz.inspect_view(view)
    return http.HttpResponse(json.dumps(data, sort_keys=True, indent=2))

def templates(request):
    data = list(find_templates())
    return http.HttpResponse(json.dumps(data, sort_keys=True, indent=2))

def template_detail(request, name):
    data = find_template(name)
    return http.HttpResponse(json.dumps(data, sort_keys=True, indent=2))
