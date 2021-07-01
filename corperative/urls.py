from django.conf.urls import patterns, include, url


urlpatterns = patterns('partner.views',
	 url(r'^partners/partner/$', 'welcome'),
	 url(r'^partner/business/reg/$','registration'),

	 )