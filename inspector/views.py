import json
from django import http
from django.shortcuts import render
import urlviz


def index(request):
    return render(request, 'inspector/index.html', {})

def url_patterns(request):
    patterns = urlviz.inspect_urlpatterns()
    return http.HttpResponse(json.dumps(patterns, sort_keys=True, indent=2))

