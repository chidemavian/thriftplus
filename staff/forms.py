from django import forms




class staffform(forms.Form):
	email = forms.EmailField(label = 'Staff Email')