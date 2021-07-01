from django.conf.urls import patterns, include, url
from sysadmin.views import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^login/$', index),
    url(r'^login/user/$', login),
    url(r'^logout/$', logoutuser),
    url(r'^changepass/$', changepass),
    url(r'^switch/$', switchuser),
    url(r'^dashboard/$', dashboard),
    # Examples:
    # url(r'^$', 'myproject.views.home', name='home'),
    url(r'^thrift/', include('thrift.urls')),
    url(r'^loans/', include('loans.urls')),
    url(r'^savings/', include('savings.urls')),
    url(r'^staff/', include('staff.urls')),
    url(r'^corperative/', include('corperative.urls')),
    url(r'^partner/', include('partner.urls')),
    url(r'^sysadmin/', include('sysadmin.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
