from django.conf.urls import patterns, include, url


urlpatterns = patterns('loans.views',
	 url(r'^loans/home/$', 'welcome'),
	 url(r'^loans/elgibility/$','eligibility'),
	 url(r'^loans/elgibility/dec/$','eligibilityyes'),

	 ####Individual Loans***************8
	 url(r'^loans/book_loan/individual/$','bookloan_individual'),

	 #####group loans ...................###
	 url(r'^loans/book_loan/creategroup/$','bookloan_creategroup'),
	 url(r'^loans/book_loan/membership/$','bookloan_membership'),
	 url(r'^loans/book_loan/bookloan/$','bookloan_bookloan'),

####***********All Ajax 
	url(r'^loans/book_loan/getlocation/$','getlocation'),
	url(r'^loans/book_loan/getgroupcode/$','getgroupcode'),
	url(r'^loans/generate/groupcode/$','generategroupcode'),
	url(r'^loans/book_loan/getgroupmembers/$', 'getgroupmembers'),
	url(r'^loans/book_loan/getgroupmembers/box/$','getgroupmembersbox'),
	url(r'^loans/book_loan/getloandetails/$','bookloandetails'),

    url(r'^loans/book_loan/getgroupmembers/approval/$','getapproved_groupmembers'),

	url(r'^loans/approvals/getcustomerdetails/$','autopostname1'),

	url(r'^loans/book_loan/getloandetails/individual/$','bookloandetails_indv'),
	url(r'^loans/book_loan/getstandardloan/$','getstandardloan'),
	url(r'^loans/book_loan/getloanparameters/$','loanparameters'),
	url(r'^loans/book_loan/getloanparametersjtjfj/$','loan_para_meters'),

############approvals###############

	 url(r'^loans/approvals/$','loanapprovals'),
	 url(r'^loans/approvals/yes/$','yesapprovaloan'),
	 url(r'^loans/termination/$', 'loantermination'),


###***************REPAYMENT*******************
	 url(r'^loans/repayment/$','loanrepay'),
	 url(r'^loans/repayment/payin/$','paybackloan'),

	 url(r'^loans/view_transaction/$','loan_view_transaction'),
	 
	 ###***************loan performance*******************

	 url(r'^loans/loan_performance/$','view_loan_performance'),
	 # url(r'^loans/defaults/$','individual'),

	 ###Settings&**************************

	 url(r'^loans/settings/$','loan_setup'),

	)
