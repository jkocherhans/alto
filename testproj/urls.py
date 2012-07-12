from django.conf.urls import *
from django.views.generic import TemplateView, RedirectView
from testproj import views

# string path
# callable function
# callable method
# callable __call__
# named
# with default args
# with url()
# using urlpatterns +=
# include
# namespaces. app:name
# args, kwargs, *args, **kwargs

urlpatterns = patterns('',
    (r'home/$', 'testproj.views.home'),
    (r'home-callable/$', views.home),

    #url(r'about/$', 'testproj.views.about'),
    #url(r'about-named/$', 'testproj.views.about', name='about'),
    #url(r'about-with-default-args/$', 'testproj.views.about', {'testing': True }),

    (r'protected/$', views.protected),
    #(r'protected-and-cached/$', views.protected_and_cached),

    #url(r'blogs/(\d+)/$', views.blog_detail),
    #url(r'blogs/(?P<slug>[\w-]+)/$', views.blog_detail),
    #url(r'blogs/(\d+)/posts/(\d+)/$', views.post_detail),
    #url(r'blogs/(?P<slug>[\w-]+)/posts/(?P<comment_id>\d+)/$', views.post_detail),

    url(r'redirect-view/$', RedirectView.as_view(url='/')),
    url(r'template-view/$', TemplateView.as_view(template_name='500.html')),

    url(r'__inspector/', include('inspector.urls')),
)
