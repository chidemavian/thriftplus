from django.conf.urls import patterns, include, url
# from thrift.views import welcome as mmm
from thrift.views import welcome as mmm

urlpatterns = patterns('sysadmin.views',
	url(r'^sysadmin/sysadmin/guide/$', 'tutorial'),

	 )