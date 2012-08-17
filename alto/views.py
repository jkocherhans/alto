import json
from django import http
from django.conf import settings
from django.shortcuts import render
from alto import urlviz
from alto.templates import find_template, find_templates


def index(request, mode=None):
    url_scheme = getattr(settings, 'ALTO_URL_SCHEME', 'mvim')
    query = request.GET.get('q', '')
    return render(request, 'alto/index.html', {
        'url_scheme': url_scheme,
        'query': query,
        'mode': mode or '',
    })

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
