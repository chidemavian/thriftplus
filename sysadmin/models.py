from django.db import models


from staff.models import *


class Userprofile(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	staffrec=models.ForeignKey(tblSTAFF)
	email=models.EmailField()
	password=models.CharField(max_length=20)
	code=models.IntegerField()
	ceo=models.BooleanField()
	
	thrift=models.BooleanField()
	thrift_officer = models.BooleanField()
	admin=models.BooleanField()
	cashier = models.BooleanField()


	loan_thrift=models.BooleanField()
	loan_thrift_admin=models.BooleanField()
	loan_thift_officer = models.BooleanField()



	savings=models.BooleanField()
	save_admin=models.BooleanField()
	account_officer = models.BooleanField()

	loan=models.BooleanField()
	loan_admin=models.BooleanField()
	loan_officer = models.BooleanField()


	coop=models.BooleanField()
	coop_admin=models.BooleanField()
	coop_officer = models.BooleanField()


	status=models.BooleanField()
	partner=models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.email,self.cashier,self.admin)

