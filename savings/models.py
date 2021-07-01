from django.db import models


from customer.models import *



class tblsavingsaccount(models.Model):
	customer=models.ForeignKey(tblCUSTOMER)
	branch=models.ForeignKey(tblBRANCH)	
	UX= models.BooleanField()
	status=models.BooleanField()
	online=models.BooleanField()
	sms=models.BooleanField()
	get_email=models.BooleanField()
	withdr_status = models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.customer,self.get_email,self.online) 




class tblsavings_trans(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	customer=models.ForeignKey(tblCUSTOMER)
	# acc=models.ForeignKey(tblsavingsaccount)
	channel=models.CharField(max_length=40)
	recdate=models.DateField()
	amount= models.IntegerField()
	code=models.CharField(max_length=40)
	kind=models.CharField(max_length=40)

	def __unicode__(self):
		return '%s %s %s'%(self.recdate,self.amount,self.code)

