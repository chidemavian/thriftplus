from django.db import models




class tblPARTNER(models.Model):
	email = models.EmailField()
	code = models.CharField(max_length=20)
	surname = models.CharField(max_length=20)
	firstname=models.CharField(max_length=20)
	othername= models.CharField(max_length=20)
	status= models.BooleanField()

	def __unicode__(self):
		return '%s %s %s'%(self.email,self.code,self.firstname)




