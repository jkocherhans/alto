import os
from django.conf.urls import *
from alto import views

urlpatterns = patterns('',
    url(r'views/([\w\d\a\._]+)/([\w\d_]+)/$', views.view_detail),
    url(r'templates/(.+)/$', views.template_detail),
    url(r'urlpatterns/$', views.url_patterns),
    url(r'template-paths/$', views.templates),
    url(r'(?P<mode>\w+)/$', views.index),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(os.path.dirname(__file__), 'static'),
    }),
    url(r'$', views.index),
)
