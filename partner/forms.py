
from django import forms

class companyform(forms.Form):
	company = forms.IntegerField(label = 'Business ID')
