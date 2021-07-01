from django.db import models



from customer.models import *


class tblmerchantBank(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	staffrec=models.ForeignKey(tblSTAFF)
	merchant=models.ForeignKey(tblMERCHANT)
	customer=models.ForeignKey(tblCUSTOMER)
	recdate=models.DateField()
	rem_date=models.DateField()
	weekno=models.IntegerField()
	amount = models.IntegerField()
	code=models.IntegerField()
	remitted_by=models.CharField(max_length=50)
	status= models.CharField(max_length=30)
	approved_by=models.CharField(max_length=50)
	# remit_time=models.TimeField()
	# approve_time=models.TimeField()

	def __unicode__(self):
		return '%s %s'%(self.recdate,self.amount)



class tblMerchantTrans(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	customer=models.ForeignKey(tblCUSTOMER)
	merchant=models.ForeignKey(tblMERCHANT)
	recdate=models.DateField()
	weekno=models.IntegerField()
	amount=models.IntegerField()
	types=models.CharField(max_length=30)
	remitted=models.CharField(max_length=30)
	approved=models.CharField(max_length=30)
	code=models.CharField(max_length=30)
	# time_in=models.TimeField()


	def __unicode__(self):
		return '%s %s %s'%(self.recdate,self.amount,self.remitted)



class tblpayoutrecord(models.Model):
	customer=models.ForeignKey(tblCUSTOMER)
	merchant=models.ForeignKey(tblMERCHANT)
	branch=models.ForeignKey(tblBRANCH)
	date=models.CharField(max_length=12)
	recdate=models.DateField(default='2021-6-12')
	status= models.CharField(max_length=20)
	amount=models.CharField(max_length=50)
	paid_by=models.CharField(max_length=90)
	month=models.CharField(max_length=20)


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.date,self.customer) 

class tblpayoutrequest(models.Model):
	customer=models.ForeignKey(tblCUSTOMER)
	merchant=models.ForeignKey(tblMERCHANT)
	branch=models.ForeignKey(tblBRANCH)
	month=models.CharField(max_length=20)
	date=models.CharField(max_length=12)
	weekno=models.IntegerField()
	status= models.CharField(max_length=20)
	code=models.IntegerField()
	amount=models.CharField(max_length=50)

	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.month,self.customer)