from django.conf.urls import patterns, include, url



urlpatterns = patterns('savings.views',
	 url(r'^savings/admin/home/$', 'welcome'),
	 url(r'^savings/openaccount/$','openaccount'),
	 url(r'^savings/withdraw/$','withdraw'),
	 url(r'^savings/deposits/$','deposit'),
	 url(r'^savings/balances/$','balances'),
	)
