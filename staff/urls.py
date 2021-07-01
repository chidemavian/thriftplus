from django.conf.urls import patterns, include, url
# from thrift.views import welcome as mmm
from thrift.views import welcome as mmm

urlpatterns = patterns('staff.views',
	url(r'^staff/staff/guide/$', 'tutorial'),
	 url(r'^staff/home/$', 'welcome'),
	 url(r'^staff/staffdet/$', 'newst'),
	 url(r'^staff/roleplay/$', 'roles'),
	 url(r'^staff/merchant/$', 'regmerchant'),
	 url(r'^staff/selectrole/$','setroles'),
	 url(r'^staff/updaterole/(\d+)/$','updaterole'),
	 url(r'^staff/viewstaffdet/$','viewdetail')
	 )