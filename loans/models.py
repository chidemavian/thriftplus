from django.db import models


from customer.models import *


class tblstandardloan(models.Model):
	staffrec=models.ForeignKey(tblSTAFF)
	branch=models.ForeignKey(tblBRANCH)
	from_week=models.CharField(max_length=20)
	rate=models.CharField(max_length=20)
	to_week=models.CharField(max_length=20)
	description=models.CharField(max_length=20)
	status=models.CharField(max_length=20)

	def __unicode__(self):
		return '%s %s %s'%(self.rate,self.description,self.from_week)


class tbleligibility(models.Model):
	staffrec=models.ForeignKey(tblSTAFF)
	branch=models.ForeignKey(tblBRANCH)
	wallet=models.CharField(max_length=20)
	status=models.CharField(max_length=20)


	def __unicode__(self):
		return '%s %s %s'%(self.status,self.wallet,self.branch)


class tblLOANGROUPS(models.Model):
	staffrec=models.ForeignKey(tblSTAFF)
	branch=models.ForeignKey(tblBRANCH)
	status=models.CharField(max_length=20)
	group=models.CharField(max_length=20)
	location=models.CharField(max_length=20)


	def __unicode__(self):
		return '%s %s %s'%(self.status,self.location,self.branch)

class tblLOANGROUPMEMBERSHIP(models.Model):
	staffrec=models.ForeignKey(tblSTAFF)
	group=models.ForeignKey(tblLOANGROUPS)
	customer=models.ForeignKey(tblCUSTOMER)


	def __unicode__(self):
		return '%s %s %s'%(self.group,self.customer,self.staffrec)




class tblloandetails(models.Model):
	branch=models.ForeignKey(tblBRANCH)
	customer=models.ForeignKey(tblCUSTOMER)
	date =models.CharField(max_length=20)
	staffrec=models.ForeignKey(tblSTAFF)
	package=models.ForeignKey(tblstandardloan)
	status=models.CharField(max_length=20)
	volume=models.CharField(max_length=20)
	thrift=models.CharField(max_length=20)
	group=models.ForeignKey(tblLOANGROUPS)

	def __unicode__(self):
		return '%s %s %s'%(self.branch,self.volume,self.package)


class tblloantransaction(models.Model):
	transaction_source=models.ForeignKey(tblloandetails)
	start_date=models.CharField(max_length=20)
	status=models.CharField(max_length=20)
	amount=models.CharField(max_length=20)
	# wallet=models.CharField(max_length=20)


	def __unicode__(self):
		return '%s %s %s'%(self.amount,self.start_date,self.status)