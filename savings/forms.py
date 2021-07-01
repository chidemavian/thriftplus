from django import forms
from loans.models import *





loan_type = ( 

	('---', '--------'),
	('Standard','Standard'), 
	('Custom','Custom'), 

	)



monthy = (('---','----'),('January','January'),('February','February'),('March','March'),('April', 'April'),
	('May','May'),('June','June'),('July','July'),('August', 'August'),('September','September'),
	('October','October'),('November', 'November'),('December','December'))


month = (('-','----'),(1,'January'),(2,'February'),(3,'March'),(4, 'April'),
	(5,'May'),(6,'June'),(7,'July'),(8, 'August'),(9,'September'),
	(10,'October'),(11, 'November'),(12,'December'))


class eligibilityform(forms.Form):
	wallet = forms.IntegerField(label = 'Wallet Address')
	amount = forms.IntegerField(label = 'Amount')



class creategroup(forms.Form):
	wallet = forms.IntegerField(label = 'Wallet Address')
	group_code = forms.CharField(label = "Group Code",max_length = 20,widget = forms.TextInput(attrs={'readonly':'readonly'}))
	location = forms.CharField(label='Location',max_length= 190)


class individualform(forms.Form):
	wallet = forms.IntegerField(label = 'Wallet Address')
	Type = forms.ChoiceField(label = 'Loan Type', choices=loan_type)


class membershipform(forms.Form):
	wallet = forms.IntegerField(label = 'Wallet Address')
	location = forms.ChoiceField(label = 'Location', choices = [(c.location, c.location) for c in tblLOANGROUPS.objects.all()])
	group_code = forms.ChoiceField(label = 'Group Code', choices=[(c.group, c.group) for c in tblLOANGROUPS.objects.all()])

class grouploanform(forms.Form):
	location = forms.ChoiceField(label = 'Location', choices = [(c.location, c.location) for c in tblLOANGROUPS.objects.all()])
	group_code = forms.ChoiceField(label = 'Group Code', choices=loan_type)
	members = forms.ChoiceField(label = 'Group Members', choices = [(c.customer.wallet, c.customer.wallet) for c in tblLOANGROUPMEMBERSHIP.objects.all()])
	Type = forms.ChoiceField(label = 'Loan Type', choices=loan_type)
	rate = forms.IntegerField(label = 'Interest Rate')
	duration = forms.IntegerField(label = 'Duration')
	volume = forms.IntegerField(label = 'Amount')
	

class loanpackages(forms.Form):
	package = forms.ChoiceField(label = 'Available Loan Packages', choices=[(c.description, c.description) for c in tblstandardloan.objects.all().order_by('id')])

class loanapproveform(forms.Form):
	wallet = forms.IntegerField(label = 'Wallet Address')

class approveloangroupform(forms.Form):
	location = forms.ChoiceField(label = 'Location', choices = [(c.location, c.location) for c in tblLOANGROUPS.objects.all()])
	group_code = forms.ChoiceField(label = 'Group Code', choices=loan_type)
	members = forms.ChoiceField(label = 'Group Members', choices = [(c.customer.wallet, c.customer.wallet) for c in tblLOANGROUPMEMBERSHIP.objects.all()])



class viewwalletform(forms.Form):
	wallet = forms.IntegerField(label = 'Wallet Address')