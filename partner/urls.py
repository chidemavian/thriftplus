from django.conf.urls import patterns, include, url


urlpatterns = patterns('partner.views',
	 url(r'^partners/partner/$', 'welcome'),
	 url(r'^partner/business/reg/$','registration'),
	 url(r'^partner/business/branch/$','branch'),
	 url(r'^partner/business/branch1/$','branch1'),		
	 url(r'^partner/business/address/$','address'),
	 url(r'^partner/business/ceo/$','ceo'),
	 url(r'^partner/business/ceo1/$','ceo1'),
	url(r'^partner/business/ceodetails/$','regceo'),

	 )