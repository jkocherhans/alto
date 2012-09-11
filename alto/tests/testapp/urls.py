from django.conf.urls import *
from alto.tests import views


urlpatterns = patterns('',
    url(r'basic_view/$', views.basic_view),
    url(r'function_decorated_view/$', views.function_decorated_view),
)
