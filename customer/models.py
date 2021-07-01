from django.db import models

from staff.models import *



class tblCUSTOMER(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	merchant=models.ForeignKey(tblMERCHANT)
	surname=models.CharField(max_length=20)
	firstname=models.CharField(max_length=20)
	othername=models.CharField(max_length=20)
	wallet=models.IntegerField()
	phone=models.IntegerField()
	Address=models.CharField(max_length=200)
	photo=models.ImageField(upload_to='company_logo', null=True,blank=True,default='studentpix/user.png')
	email=models.EmailField()
	UX= models.BooleanField()
	status=models.BooleanField()
	online=models.BooleanField()
	code=models.IntegerField()
	sms=models.BooleanField()
	get_email=models.BooleanField()
	withdr_status=models.BooleanField()


	def __unicode__(self):
		return '%s %s %s'%(self.surname,self.firstname,self.code) 

class tblthrift(models.Model):
	customer=models.ForeignKey(tblCUSTOMER)
	merchant=models.ForeignKey(tblMERCHANT)
	branch=models.ForeignKey(tblBRANCH)
	month=models.CharField(max_length=20)
	thrift=models.IntegerField()
	code=models.IntegerField()
	number=models.IntegerField()
	year=models.CharField(max_length=20)


	def __unicode__(self):
		return '%s %s %s'%(self.number,self.month,self.code)


class tblthrift_trans(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	merchant=models.ForeignKey(tblMERCHANT)
	customer=models.ForeignKey(tblCUSTOMER)
	number=models.IntegerField()
	recdate=models.DateField()
	amount= models.IntegerField()
	types=models.CharField(max_length=40)
	avalability=models.CharField(max_length=50)
	reason=models.CharField(max_length=40)
	code=models.CharField(max_length=40)

	def __unicode__(self):
		return '%s %s %s'%(self.recdate,self.amount,self.reason)

