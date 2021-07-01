
from __future__ import division

from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from loans.forms import *

from sysadmin.models import *
from customer.models import *
from merchant.models import *
from loans.models import *
from savings.models import *




from datetime import *
import calendar

from calendar import monthrange

from django.core.serializers.json import json

from django.db.models import Max,Sum

import random

today=date.today()


def welcome(request):
	if 'userid' in request.session:

		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		
		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		

		return render_to_response('loans/welcome.html',{'company':mybranch, 'user':varuser})
	
	else:
		return HttpResponseRedirect('/login/')



def eligibility(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		
		staffdet=staff.staffrec.id

		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		varuser=tblSTAFF.objects.get(email=varuser)

		thrifts_details=[]
		
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = eligibilityform(request.POST)
			tot=0		

			if form.is_valid():
				wallet =form.cleaned_data['wallet']

				try : 
					
					customer= tblCUSTOMER.objects.get(wallet=wallet,branch=mybranch,status=1)
					for x in range(1,13) : 
						
						try : 
							thrifts=tblthrift.objects.get(customer=customer,number=x)
							mmy=thrifts.thrift
							thrift_trans = tblthrift_trans.objects.filter(customer=customer,recdate__month = x,avalability='Available')
							kkk = thrift_trans.count()

							if kkk > 0 : 
								number=thrift_trans.aggregate(Sum('number'))
								number = number['number__sum']

								amount=thrift_trans.aggregate(Sum('amount'))
								amount = amount['amount__sum']
								status='Available'

							else:
								withdrr= tblpayoutrecord.objects.filter(customer=customer,recdate__month=x)
								kkk2 = withdrr.count()

								if kkk2 > 0 : 									
									amount=withdrr.aggregate(Sum('amount'))
									amount = amount['amount__sum']
									number = int(amount / mmy)
									status='Withdrawn'

							
							tot=tot+amount	

							monthname = calendar.month_name[int(x)]

							jko = {'thrift':thrifts,'month':monthname,'total':amount,'count':number, 'status':status}
							thrifts_details.append(jko)

						except : 
							thrifts= 0
							number=0
							amount=0
							status=0

					
					cr_savings=tblsavings_trans.objects.filter(customer=customer,branch=mybranch,kind='CR')
					dr_savings=tblsavings_trans.objects.filter(customer=customer,branch=mybranch,kind='DR')


					kkk2 = cr_savings.count()

					if kkk2 > 0 : 
						cr_sum=cr_savings.aggregate(Sum('amount'))
						cr_sum = cr_sum['amount__sum']
					else:
						cr_sum=0

					kkk2 = dr_savings.count()

					if kkk2 > 0 : 
						dr_sum=dr_savings.aggregate(Sum('amount'))
						dr_sum = dr_sum['amount__sum']

					else:
						dr_sum=0

					balance = cr_sum - dr_sum 


					return render_to_response('loans/eligibility_check.html',{'company':mybranch, 'user':varuser,'wallet':wallet,
						'msg':thrifts_details,'branch':branch,'tot':tot,'withdraw':customer,'cr':cr_sum,'dr':dr_sum,'balance':balance})

				except : 
					msg = 'Check wallet Address'
			
			else : 
				return HttpResponseRedirect('/dashboard/')

		else:
			form=eligibilityform()
			msg=''
			
		return render_to_response('loans/eligibility.html',{'company':mybranch, 'user':varuser,
			'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')

def eligibilityyes(request): 

	varuser=request.session['userid']
	staff = Userprofile.objects.get(email=varuser,status=1)

	
	staffdet=staff.staffrec.id

	branch=staff.branch.id

	mycompany=staff.branch.company
	company=mycompany.name
	comp_code=mycompany.id
	ourcompay=tblCOMPANY.objects.get(id=comp_code)

	mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
	varuser=tblSTAFF.objects.get(email=varuser)
		
	if 'gender'  in request.POST: 

		dec = request.POST['gender']
		wallet=request.POST['wallet']
		branch=request.POST['branch']

		mybranch=tblBRANCH.objects.get(id=branch)


		if dec == 'yes': 
			try: 
				elib = tbleligibility.objects.get(wallet=wallet,branch=mybranch,status='Eligible')
				msg = 'customer already in eligibility list'
			
			except: 
				msg = 'Customer is Eligible'
				tbleligibility(wallet=wallet,
					staffrec=varuser,
					branch=mybranch,
					status='Eligible').save()
		else : 
			msg = 'Not Eligible'
	

		return render_to_response('loans/eligibility_outcome.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		form=eligibilityform()
		msg=''
		
		return render_to_response('loans/eligibility.html',{'company':mybranch, 'user':varuser,
			'form':form,'msg':msg})


def bookloan_individual(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = individualform(request.POST)

			if form.is_valid():
				merchant =form.cleaned_data['merchant']
				mydate2=form.cleaned_data['date'] #JavaScript Date Object
				

			else:
				pass
       
		else:
			form=individualform()
			msg=''
		return render_to_response('loans/bookindividualloan.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')


def bookloan_creategroup(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		mmm = tblSTAFF.objects.get(email=varuser,branch=mybranch)
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = creategroup(request.POST)

			if form.is_valid():
				wallet =form.cleaned_data['wallet']
				location=form.cleaned_data['location']
				gcode = form.cleaned_data['group_code']

				if gcode != 'OOPS!' : 

					try:
						customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)
						loan_customer = tbleligibility.objects.get(wallet=wallet,branch=mybranch,status='Eligible')
						membership= tblLOANGROUPMEMBERSHIP.objects.filter(customer=customer)
						membership_count = membership.count()

						#### Check for prior membership***********
						if membership_count == 0 : 
							tblLOANGROUPS(staffrec=mmm,branch=mybranch,group=gcode,location=location, status='Active').save()
							group_id = tblLOANGROUPS.objects.get(staffrec=mmm,branch=mybranch,group=gcode,location=location, status='Active')
							tblLOANGROUPMEMBERSHIP(group=group_id,customer=customer,staffrec=mmm).save()
							msg = 'group created successfully. One member added' 
							return render_to_response('loans/create_group_success.html',{'company':mybranch, 'user':varuser,'location':location,'gcode':gcode,'member':customer,'msg':msg})
					
						else:
							msg = "Customer cannot join this group"
					
					except :
						msg = 'check the wallet'
					
					# return render_to_response('loans/create_group_success.html',{'company':mybranch, 'user':varuser,'location':location,'gcode':gcode,'member':customer,'msg':msg})
				
				else :  
					msg = " Click the plus sign again"

			else : 
				msg = 'fill up all boxes'       
		else:
			form=creategroup()
			msg=''
		return render_to_response('loans/creategroup.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')


def generategroupcode(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                acccode,wallet=acccode.split(":")
                acccode= acccode[0:3].upper()
                if acccode !='' and wallet !='':
                	todays=date.today()
                	myear=todays.year
                	k = random.randint(0,9)
                	y = random.randint(0,9)
                	x = random.randint(0,9)
                	z = random.randint(0,9)
                	a = random.randint(0,9)
                	pin =  str(k) + str(y) + str(x) + str(z)+ str(a)
                	gc = '%s/%s/%s'%( acccode, myear,pin)
                	return HttpResponse(json.dumps(gc), mimetype='application/json')

                else:
	            	gc= 'OOPS!'
	            	return HttpResponse(json.dumps(gc), mimetype='application/json')


        else:
        	gdata = ""
        	return render_to_response('getlg.htm',{'gdata':gdata})
    else:
    	return HttpResponseRedirect('/login/')



def bookloan_membership(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		mmm = tblSTAFF.objects.get(email=varuser,branch=mybranch)
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = membershipform(request.POST)
			msg = ''

			if form.is_valid():
				location =form.cleaned_data['location']
				group_code=form.cleaned_data['group_code']
				wallet = form.cleaned_data['wallet']

				g_code=tblLOANGROUPS.objects.get(group=group_code)

				
				try:
					customer=tblCUSTOMER.objects.get(wallet=wallet,branch=mybranch,status=1)
					

					try:
						loan_customer = tbleligibility.objects.get(wallet=wallet,branch=mybranch,status='Eligible')

						
						try:
							member = tblLOANGROUPMEMBERSHIP.objects.get(customer=customer)
							msg = 'customer already belongs in a group'
						
						except : 

							tblLOANGROUPMEMBERSHIP(group=g_code ,customer=customer,staffrec=mmm).save()

							return render_to_response('loans/addmember_success.html',{'company':mybranch, 'user':varuser})
						

					except :
						msg = 'customer not eligible' 
					
				
				except : 
					msg = 'not a customer'
				
			else : 
				return HttpResponseRedirect('/dashboard/')
       
		else:
			form=membershipform()
			msg=''
		return render_to_response('loans/membership.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')


def getlocation(request):
	if  "userid" in request.session:
		if request.is_ajax():
			if request.method == 'POST':

				varuser = request.session['userid']
				staff = Userprofile.objects.get(email=varuser,status=1)
				# staffdet=staff.staffrec.id
				branch=staff.branch.id
				mybranch=tblBRANCH.objects.get(id=branch)

				post = request.POST.copy()
				acccode = post['userid']
				kk = []
				sdic = {}
				grpss = tblLOANGROUPS.objects.filter(branch=mybranch)
				grpss_count = grpss.count()

				if grpss_count > 0 :

					for j in grpss:
						j = j.location
						s = {j:j}
						sdic.update(s)
						klist = sdic.values()
					for p in klist:
						kk.append(p)
				else : 
					kk.append("OOPS!!!")
				return HttpResponse(json.dumps(kk), mimetype='application/json')
			else:
				gdata = ""
				return render_to_response('index.html',{'gdata':gdata})
        else:
        	gdata = ""
        	return render_to_response('getlg.htm',{'gdata':gdata})



def getgroupcode(request):
	if  "userid" in request.session:
		if request.is_ajax():
			if request.method == 'POST':

				varuser = request.session['userid']
				staff = Userprofile.objects.get(email=varuser,status=1)
				staffdet=staff.staffrec.id
				branch=staff.branch.id
				mybranch=tblBRANCH.objects.get(id=branch)


				post = request.POST.copy()
				acccode = post['userid']
				kk = []
				sdic = {}
				grpss = tblLOANGROUPS.objects.filter(branch=mybranch,location=acccode)
				gcount= grpss.count()
				if gcount > 0 :

					for j in grpss:
						j = j.group
						s = {j:j}
						sdic.update(s)
						klist = sdic.values()
					for p in klist:
						kk.append(p)
				else : 
					kk.append('NO GROUPS FOUND')
				return HttpResponse(json.dumps(kk), mimetype='application/json')
			else:
				gdata = ""
				return render_to_response('index.html',{'gdata':gdata})
        else:
        	gdata = ""
        	return render_to_response('getlg.htm',{'gdata':gdata})
 


def getgroupmembers(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                location,group = acccode.split(':')

                getcode = tblLOANGROUPS.objects.filter(group=group,location=location)
                gtco = getcode.count()
                if gtco > 0 : 
                	getcode = tblLOANGROUPS.objects.filter(group=group,location=location)
                	getmember = tblLOANGROUPMEMBERSHIP.objects.filter(group=getcode).order_by('customer')
	                return render_to_response('loans/mygroupmemberlist.html',{'data':getmember,'group':group,'location':location})
            	else:
            		msg = 'No locations found'
            		return render_to_response('loans/ngl.html',{'msg':msg})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')
      

def bookloandetails(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                location,group,customer,Type,user= acccode.split(':')
                form = loanpackages()


                if Type == "---":
                	return render_to_response('loans/selectloan.html')

                elif Type== 'Custom':
                	return render_to_response('loans/customloan.html',{'group':group,'location':location})
                 
                
                getcode = tblLOANGROUPS.objects.get(group=group,location=location)
                loancustomer=tblCUSTOMER.objects.get(wallet=customer,status=1)
                getmember = tblLOANGROUPMEMBERSHIP.objects.filter(customer=loancustomer, group=getcode).order_by('customer')
 
                try : 
                	eree = tblloandetails.objects.get(customer=loancustomer,status='Not Approved')
                	eded='Booked' 
                	return render_to_response('loans/bookeddetails.html',{'data':eree,'user':user,'status':eded,'group':group,'location':location})
                except : 
                	eded= 'Not booked' 
                	return render_to_response('loans/standardloan.html',{'data':getmember,'group':group,'location':location,'form':form,'user':user,'status':eded})
               
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def loan_para_meters(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                
                customer, user= acccode.split(':')
                
                staff = Userprofile.objects.get(email=user,status=1)
              
                branch=staff.branch.id

                mybranch=tblBRANCH.objects.get(id=branch)

               	my_client= tblCUSTOMER.objects.get(wallet=customer,status=1)

               	
               	pos= tblloandetails.objects.get(customer=my_client,status='Not Approved')
               	# runn = pos.status
               	return render_to_response('loans/running_loan.html',{'data':pos,'user':user})
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')

def bookloandetails_indv(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                wallet,Type= acccode.split(':')
                form = loanpackages()

                if Type == "---":
                	return render_to_response('loans/selectloan.html')
                
                
                getcode = tbleligibility.objects.filter(wallet=wallet)
                
                if getcode.count() > 0:
                	loancustomer=tblCUSTOMER.objects.get(wallet=customer,status=1)
	                getmember = tblLOANGROUPMEMBERSHIP.objects.filter(customer=loancustomer, group=getcode).order_by('customer')
	                

	   #              if Type == 'Standard':
	                              	
	   #              	return render_to_response('loans/standardloan.html',{'data':getmember,'group':group,'location':location,'form':form,'user':user})
	               
	   #              elif Type== 'Custom':
	   #              	return render_to_response('loans/customloan.html',{'data':getmember,'group':group,'location':location})

	   #         else:
	   #         	jhh=7

    #         else:
    #             gdata = ""
    #             return render_to_response('index.html',{'gdata':gdata})
    #     else:
    #         gdata = ""
    #         return render_to_response('getlg.htm',{'gdata':gdata})
    # else:
    #     return HttpResponseRedirect('/login/')



def loanparameters(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                
                package,customer, user= acccode.split(':')
                
                staff = Userprofile.objects.get(email=user,status=1)
              
                branch=staff.branch.id

                mybranch=tblBRANCH.objects.get(id=branch)

                getcode = tblstandardloan.objects.get(description=package,branch=mybranch)

               	my_client= tblCUSTOMER.objects.get(wallet=customer,status=1)


               	try : 
               		pos= tblloandetails.objects.get(customer=my_client)
               		runn = pos.status
               		if runn== 'Running': 
               			return render_to_response('loans/running_loan.html',{'data':pos,'user':user})
               		elif runn == 'Not Approved' : 
               			return render_to_response('loans/running_loan.html',{'data':pos,'user':user})
               		elif runn == 'Paid' : 
               			return render_to_response('loans/running_loan.html',{'data':pos,'user':user})
               	except : 

               		if package== '-----': 
               			return render_to_response('loans/nopackage.html',{'data':getcode,'user':user,'package':package})
	                
	                else:
	                	return render_to_response('loans/loanparameters.html',{'data':getcode,'user':user,'package':package})

            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')


def getgroupmembersbox(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                location,group = acccode.split(':')
                sdic={}
                kk=[]
                getcode = tblLOANGROUPS.objects.get(group=group,location=location)
                getmember = tblLOANGROUPMEMBERSHIP.objects.filter(group=getcode)
          
                if getmember.count()==0:
                	return render_to_response('loans/nullmember.html')#,{'data':getmember,'group':group,'location':location,'form':form})
               
                else:
	                for j in getmember:
	                	j = j.customer.wallet
	                	s = {j:j}
	                	sdic.update(s)
	                	klist = sdic.values()
                	for p in klist:
                		kk.append(p)
           
	                return HttpResponse(json.dumps(kk), mimetype='application/json')
	else:
		return HttpResponseRedirect('/login/')



def getapproved_groupmembers(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                location,group = acccode.split(':')
                sdic={}
                kk=[]
                getcode = tblLOANGROUPS.objects.get(group=group,location=location)
                getmember = tblLOANGROUPMEMBERSHIP.objects.filter(group=getcode)
          
                if getmember.count()==0:
                	return render_to_response('loans/nullmember.html')#,{'data':getmember,'group':group,'location':location,'form':form})
               
                else:
	                for j in getmember:
	                	j = j.customer.wallet
	                	s = {j:j}
	                	sdic.update(s)
	                	klist = sdic.values()
                	for p in klist:
                		kk.append(p)
           
	                return HttpResponse(json.dumps(kk), mimetype='application/json')
	else:
		return HttpResponseRedirect('/login/')

def getstandardloan(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']

                staff = Userprofile.objects.get(email=acccode,status=1)
                staffdet=staff.staffrec.id
                branch=staff.branch.id

                mycompany=staff.branch.company
                company=mycompany.name
                comp_code=mycompany.id
                ourcompay=tblCOMPANY.objects.get(id=comp_code)
                mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

                sdic={}
                kk=[]
                getcode = tblstandardloan.objects.filter(branch=mybranch)
                if getcode.count()==0:
                	return render_to_response('loans/nullmember.html')
               
                else:
	                for j in getcode:
	                	j = j.description
	                	s = {j:j}
	                	sdic.update(s)
	                	klist = sdic.values()
                	for p in klist:
                		kk.append(p)                
	                kk.sort()
	                return HttpResponse(json.dumps(kk), mimetype='application/json')
	else:
		return HttpResponseRedirect('/login/')





def bookloan_bookloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		
		msg =''
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = grouploanform(request.POST)

			# if form.is_valid():
			location =request.POST['location']
			group_code=request.POST['group_code']
			members=request.POST['members']
			Type=request.POST['Type']
			rate=request.POST['rate']
			duration=request.POST['duration']
			volume=request.POST['volume']
			package=request.POST['package']

			package=tblstandardloan.objects.get(description=package)
			group_code=tblLOANGROUPS.objects.get(group=group_code)

			customer=tblCUSTOMER.objects.get(wallet=members,status=1)

			fdate= datetime.today()
			todayy=date(fdate.year,fdate.month,fdate.day)
				
			rate=int(rate)
			duration=int(duration)
			volume=int(volume)

			thrift_com = (100+rate) * volume /  100
			thrifty = int(thrift_com / duration)


			
			loan_det = tblloandetails.objects.filter(branch=mybranch,customer=customer,date=todayy,
				staffrec=memstaff,package=package,status='Not Approved',volume=volume,thrift=thrifty,group=group_code)

			loan_count = loan_det.count()

			if loan_count == 0 : 
				tblloandetails(branch=mybranch,customer=customer,date=todayy,staffrec=memstaff,package=package,status='Not Approved',volume=volume,thrift=thrifty,group=group_code).save()
				return render_to_response('loans/booking_success.html',{'company':mybranch, 'user':varuser,'customer':customer})
			else : 
				return HttpResponseRedirect('/loans/loans/book_loan/bookloan/')
		else:
			form=grouploanform()
			msg=''
		return render_to_response('loans/bookgrploan.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def loanapprovals(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		form=approveloangroupform()
		msg=''
		return render_to_response('loans/loanapprove.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/')


def autopostname1(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                location,group,customer= acccode.split(':')
                form = loanpackages()

                if customer == '---' : 
                	return render_to_response('loans/customloan.html',{'data':getmember,'group':group,'location':location})

                else :                 	
	                getcode = tblLOANGROUPS.objects.get(group=group,location=location)
	                loancustomer=tblCUSTOMER.objects.get(wallet=customer,status=1)
	                getmember = tblLOANGROUPMEMBERSHIP.objects.filter(customer=loancustomer, group=getcode).order_by('customer')

                ######check booking***************
	                try : 

	                	details = tblloandetails.objects.get(customer=loancustomer)
	                	sfsd= tblloantransaction.objects.filter(transaction_source=details)
	                	book_count = int(sfsd.count())

	                except : 
	                	msg='loan not booked'
	                	
	                	return render_to_response('loans/not_booked_loan.html',{'data':msg})
				 	
	                
	                if book_count < 1 : 
	                	return render_to_response('loans/processloan.html',{'details':details,'wallet':customer})
	                	
	                else : 
	                	msg='loan approved already' 
		            	return render_to_response('loans/loan_approved.html',{'details':details,'wallet':customer})
		           
            else:
                gdata = ""
                return render_to_response('index.html',{'gdata':gdata})
        else:
            gdata = ""
            return render_to_response('getlg.htm',{'gdata':gdata})
    else:
        return HttpResponseRedirect('/login/')





def yesapprovaloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		fdate= datetime.today()

		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST': 
			wallet =request.POST['wallet']
		 	customer=tblCUSTOMER.objects.get(wallet=wallet,branch=mybranch,status=1)
		 	details = tblloandetails.objects.get(customer=customer)

		 	thrift=(details.thrift)
		 	duration= int(details.package.to_week)
		 	duration=duration+1
		 	volume=details.volume

		 	trans = tblloantransaction.objects.filter(transaction_source=details,start_date=fdate, status='DR',amount=thrift)
		 	trans_count= trans.count()
		 	if trans_count== 0 :		 		
			 	for n in range (1,duration):  
			 		tblloantransaction(transaction_source=details,start_date=fdate, status='DR',amount=thrift).save()
			 	details = tblloandetails.objects.filter(customer=customer).update(status='Running')
				return render_to_response('loans/approveloan_success.html',{'company':mybranch, 'user':varuser,'sum':volume,'customer':customer})     
		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/')


def loanrepay(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = loanapproveform(request.POST)

			if form.is_valid():
				wallet =form.cleaned_data['wallet']
				customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)
				details=tblloandetails.objects.get(customer=customer)
				dr=tblloantransaction.objects.filter(transaction_source=details, status='DR').count()
				cr=tblloantransaction.objects.filter(transaction_source=details,status='CR').count()
				dr1= int(dr)-int(cr)
				
				if dr > 0 : 
					if details.status=='Paid' : 
						return render_to_response('loans/paid.html',{'company':mybranch, 'user':varuser,'details':details,'wallet':wallet,'debit':dr,'credit':cr,'rem':dr1})
					else : 
						return render_to_response('loans/repayloanprocess.html',{'company':mybranch, 'user':varuser,'details':details,'wallet':wallet,'debit':dr,'credit':cr,'rem':dr1})
				else:
					msg = 'no details found'
		else:
			form=loanapproveform()
			msg=''
		return render_to_response('loans/repayloan.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')


def paybackloan(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		fdate= datetime.today()
		recdate=date(fdate.year,fdate.month,fdate.day)
	
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST': 
			wallet =request.POST['wallet']
			amount=request.POST['amount']
		 	customer=tblCUSTOMER.objects.get(wallet=wallet,branch=mybranch,status=1)
		 	details = tblloandetails.objects.get(customer=customer)
		 	thrift=details.thrift
		 	thrift=float(thrift)
		 	amount=int(amount)

			dr=tblloantransaction.objects.filter(transaction_source=details, status='DR').count()
			cr=tblloantransaction.objects.filter(transaction_source=details,status='CR').count()
			
			limit= int(dr)-int(cr)
		 	a,b=divmod(amount,thrift)
		 	a=int(a)

		 	loans = a * thrift

		
# this is a case of whats left vs whats coming in

		 	if a  < 1 : 
		 		return HttpResponseRedirect('/loans/loans/repayment/')
		 	else : 

		 		if limit >= a : 

				 	if a > 0 : 
				 		
				 		duration= a + 1

					 	for n in range (1,duration):  
					 		tblloantransaction(transaction_source=details,
					 			start_date=fdate, status='CR',amount=thrift).save()
						
				 	else : # still thinking
				 		pass


				elif limit < a : 
					duration = limit + 1

				 	for n in range (1,duration):  
				 		tblloantransaction(transaction_source=details,
				 			start_date=fdate, status='CR',amount=thrift).save()
				
					details = tblloandetails.objects.filter(customer=customer).update(status='Paid')
			 

					b = b + ((a-limit ) * thrift)

	###Throwing b into savings account.................
				tblsavings_trans(customer=customer,branch=mybranch,
					amount=b,code='3342',recdate=recdate,kind='CR',channel = 'Offline').save()

				# tblsavingstransaction(customer=customer,branch=mybranch,
					# merchant=merchant,amount=b,code=code,recdate=recdate,channel = 'Offline').save()


				return render_to_response('loans/repay_loan_sucess.html',{'company':mybranch, 'user':varuser,'loan':loans,'savings':b})


		else:
			return HttpResponseRedirect('/dashboard/')

	else:
		return HttpResponseRedirect('/login/')



def loantermination(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = loanapproveform(request.POST)

			if form.is_valid():
				wallet =form.cleaned_data['wallet']
				try : 
				 	customer=tblCUSTOMER.objects.get(wallet=wallet,branch=mybranch,status=1)
				 	details = tblloandetails.objects.get(customer=customer)

				 	return render_to_response('loans/terminateloan.html',{'company':mybranch, 'user':varuser,'details':details})
				except: 
				 	sef = ''
			else : 
				msg = 'invalid wallet'

				 	
       
		else:
			form=loanapproveform()
			msg=''
		return render_to_response('loans/loanapprove.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/')





def loan_view_transaction(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = loanapproveform(request.POST)

			if form.is_valid():
				wallet =form.cleaned_data['wallet']
			else:
				pass
       
		else:
			form=loanapproveform()
			msg=''
		return render_to_response('loans/view_transaction.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')




def view_loan_performance(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = loanapproveform(request.POST)

			if form.is_valid():
				wallet =form.cleaned_data['wallet']
				customer=tblCUSTOMER.objects.get(wallet=wallet,status=1)
				details=tblloandetails.objects.get(customer=customer)
				dr=tblloantransaction.objects.filter(transaction_source=details, status='DR')
				
				return render_to_response('loans/loan_performance.html',{'company':mybranch, 'user':varuser,'dr':dr})
								
			

			else:
				pass
       
		else:
			form=loanapproveform()
			msg=''
		return render_to_response('loans/view_performance.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



##Settings******************




def loan_setup(request):
	if 'userid' in request.session: 
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		loans = tblstandardloan.objects.filter(branch=mybranch)
		user=tblSTAFF.objects.get(email=varuser)

		if staff.cashier==0: 
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST': 
			description=request.POST['package']
			rate= request.POST['rate']
			fromm= request.POST['fromm']
			to= request.POST['to']
			pack_count=loans.count()
			
			if pack_count == 0 : 
				tblstandardloan(rate = 0 ,description='-----', staffrec=user,branch=mybranch,status='ACTIVE',from_week=0,to_week=0).save()
				tblstandardloan(rate = rate ,description=description, staffrec=user,branch=mybranch,status='ACTIVE',from_week=fromm,to_week=to).save()
			else: 
				tblstandardloan(rate = rate ,description=description, staffrec=user,branch=mybranch,status='ACTIVE',from_week=fromm,to_week=to).save()
			msg = "package added successfully"
			return render_to_response('loans/addpackage.html',{'company':mybranch, 'user':varuser,'msg':msg})

		return render_to_response('loans/set_uploan.html',{'company':mybranch, 'user':varuser,'loans':loans})
	else : 
		return HttpResponseRedirect('/login/')




