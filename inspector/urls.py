from django.conf.urls import *
from inspector import views

urlpatterns = patterns('',
    url(r'urlpatterns/$', views.url_patterns),
)
