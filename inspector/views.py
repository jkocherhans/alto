import json
from django import http
from django.shortcuts import render
import urlviz


def index(request):
    return render(request, 'inspector/index.html', {})

def url_patterns(request):
    patterns = urlviz.inspect_urlpatterns()
    return http.HttpResponse(json.dumps(patterns, sort_keys=True, indent=2))

def view_detail(request, module_path, view_name):
    view = urlviz.load_view(module_path, view_name)
    view, decorators = urlviz.extract_view(view)
    data = urlviz.inspect_view(view)
    return http.HttpResponse(json.dumps(data, sort_keys=True, indent=2))
