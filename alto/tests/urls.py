from django.conf.urls import *
from alto.tests import views

urlpatterns = patterns('',
    (r'^basic_view/$', views.basic_view),
    url(r'^function_decorated_view/$', views.function_decorated_view),
    url(r'^instance_decorated_view/$', views.instance_decorated_view),
    url(r'^testapp/', include('alto.tests.testapp.urls')),
)
