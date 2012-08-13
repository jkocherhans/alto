from django.conf.urls import *
from alto import views

urlpatterns = patterns('',
    url(r'urlpatterns/$', views.url_patterns),
    url(r'templates/$', views.templates),
    url(r'views/([\w\d\a\._]+)/([\w\d_]+)/$', views.view_detail),
    url(r'$', views.index),
)
