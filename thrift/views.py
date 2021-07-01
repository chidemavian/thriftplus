from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from django.core.serializers.json import json
from thrift.forms import *
from sysadmin.models import *
from customer.models import *
from merchant.models import *
from savings.models import *

from datetime import *
import calendar
#######import only merchant.models******
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

		return render_to_response('thrift/welcome.html',{'company':mybranch, 'user':varuser})
	
	else:
		return HttpResponseRedirect('/login/')



def adminwelcome(request):
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

		
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
	
		return render_to_response('thrift/adminwelcome.html',{'company':mybranch, 'user':varuser})

	else:
		return HttpResponseRedirect('/login/')					

def createwallet(request):
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
		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		msg = ''

		if request.method == 'POST':
			surname=request.POST['surname']
			firstname= request.POST['firstname']
			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']


			phone=phone.split(' ')
			phone = str(phone[0]+phone[1]+phone[2])

			# if photo in request.POST:
			# 	photo=request.POST['photo']

			try:
				phone1=int(phone)

				wallet=phone1
					
				try:
					msg = 'Wallet already existing'
					countt=tblCUSTOMER.objects.get(wallet=wallet,status=1)
				
				except:

					tblCUSTOMER(surname=surname,firstname=firstname,
						othername=othername,phone=phone,Address=address,
						wallet=wallet,code=68768,email=email,withdr_status=1,
						UX=0,branch=mybranch,merchant=memmerchant,status=1,
						online=0,sms=0,
						get_email=0,
						# photo=photo
						).save()

					acc_cus=tblCUSTOMER.objects.get(surname=surname,firstname=firstname,othername=othername,
						phone=phone,Address=address,wallet=wallet,code=68768,email=email,
						UX=0,branch=mybranch,merchant=memmerchant,status=1,
						online=0,sms=0,get_email=0)

					tblsavingsaccount(customer=acc_cus,branch=mybranch,UX=0,status=1,online=0,sms=0,get_email=0,withdr_status=1).save()

					return render_to_response('thrift/success.html',{'company':mybranch,'user':varuser,'wallet':wallet})

			except:
				msg = 'Incomplete phone number'
		
		return render_to_response('thrift/createwallet.html',{'company':mybranch, 'user':varuser,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/')


def editwallet(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)


## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html')
		
		if request.method == 'POST':
			form= viewwalletform(request.POST)
			msg='Try again later'
		
			if form.is_valid():
				wallet=form.cleaned_data['wallet']
				try:
					customer=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=wallet,status=1)
					msg=''
					return render_to_response('thrift/myeditwallet.html',{'company':mybranch,
					'user':varuser,'msg':msg,'wallet':wallet,'form':form,'customer':customer})

				except:
					msg='INVALID WALLET ADDRESS'
		else:
			form = viewwalletform()
			msg=''

		return render_to_response('thrift/editwallet.html',{'company':mybranch,'user':varuser,'msg':msg,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')


def viewwallet(request):
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

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html')
			
		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				wallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(wallet=wallet,status=1)
					return render_to_response('thrift/walletdetails.html',{'company':mybranch,'user':varuser,'details':details})
				except:
					msg = 'invalide wallet address'
					return render_to_response('thrift/viewwallet.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
			else:
				pass
		else:
			form=viewwalletform()
		return render_to_response('thrift/viewwallet.html',{'company':mybranch,'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')


def thriftrep(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		

		if request.method == 'POST':
			form = unremitform(request.POST)
			if form.is_valid()==False:
				month=form.cleaned_data['month']
				if month=="-":
					pass
				else:

					monthname = calendar.month_name[int(month)]

					dll=[]				
					details=tblCUSTOMER.objects.filter(branch=mybranch, merchant=memmerchant,status=1)
					for  k in details:
						try:
							thriftrec=tblthrift.objects.get(customer=k,number=month)
							dl={'wallet':k.wallet,'thrift':thriftrec.thrift}				
						except:
							dl={'wallet':k.wallet,'thrift':0}
						dll.append(dl)

					return render_to_response('thrift/thriftrep.html',{'company':mybranch,'user':varuser,'thriftrec':dll,'month':monthname})

		else:
			form=unremitform()
		return render_to_response('thrift/repthr.html',{'company':mybranch,'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')


### THRIFT AFFAIRS*************************

def addthrift(request):
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


		if staff.thrift==0:
				return render_to_response('404.html',{'company':mybranch, 'user':varuser})


		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		

		tdate= date.today()
		mday=tdate.month
		yday=tdate.year
		month = calendar.month_name[mday] #converts to name of month


		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']

				try:
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)
					thriftrec=tblthrift.objects.get(merchant=memmerchant, month=month,customer=details,year=yday)
					return render_to_response('thrift/putthrift.html',{'company':mybranch,'user':varuser,
						'month':month,'wallet':mywallet,'thriftrec':thriftrec})
				except:
					try:
						details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)	
						myform = thriftform()
						return render_to_response('thrift/myadd.html',{'company':mybranch,'user':varuser,'form':myform,
						'wallet':mywallet})
					except:
						msg='INVALID WALLET ADDRESS'
			else:
				msg='Incorrect entry'

		else:
			form=viewwalletform()
			msg = ''
		return render_to_response('thrift/addthrift.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/')


def putthrift(request):
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

		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch,
				'user':varuser})

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch,
				'user':varuser})
	

		yday = date.today().year

		if request.method == 'POST':
			form = thriftform(request.POST)
			if form.is_valid():
				number=form.cleaned_data['month']  #returns month number as directed in form
				mythrift=form.cleaned_data['thrift']
				wallet=request.POST['wallet']

				month=calendar.month_name[int(number)] #converts month number to month name

				customer=tblCUSTOMER.objects.get(merchant=memmerchant,
					wallet=wallet,status=1)
				
				countt= tblthrift.objects.filter(month=month,branch=mybranch,
					merchant= memmerchant,customer=customer).count()

				if countt<1:
					tblthrift(month=month,thrift=mythrift,branch=mybranch,
						merchant= memmerchant,customer=customer,
						code=8797,number=number,year=yday).save()
				return render_to_response('thrift/addthriftsuccess.html',{'company':mybranch, 'user':varuser,'wallet':wallet,'thrift':mythrift,'month':month})
	else:
		return HttpResponseRedirect('/login/')



def addmythrift(request):
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

		memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)

		tdate= date.today()
		mday=tdate.month
		month = calendar.month_name[mday]
		myform = kthriftform()


		if request.method == 'POST':
			mywallet=request.POST['wallet']
			myform = kthriftform(request.POST)
			details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)	
			return render_to_response('thrift/comeadd.html',{'company':mybranch,'user':varuser,'form':myform,
			'wallet':mywallet,'month':month})
		else:
			return HttpResponseRedirect('/login/')


def putinthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		
		if request.method == 'POST':
			form = kthriftform(request.POST)
			if form.is_valid():
				month=request.POST['month']  # month in words
				mythrift=form.cleaned_data['thrift']
				wallet=request.POST['wallet']

				today=date.today()
				yday=today.year

				month1 = datetime.strptime(month,"%B") #month to number
				month2=month1.month
				customer=tblCUSTOMER.objects.get(merchant=memmerchant,wallet=wallet,
					status=1)
				
				tblthrift(month=month,year=yday,thrift=mythrift,branch=mybranch,
					merchant= memmerchant,customer=customer,
					code=8797,number=month2).save()

				return render_to_response('thrift/addthriftsuccess.html',{'company':mybranch, 'user':varuser,'wallet':wallet,'thrift':mythrift,'month':month})
			else:
				msg = 'im me'
				return render_to_response('thrift/comeadd.html',{'msg':month})

		else:
			return HttpResponseRedirect('/login/')

	else:
		return HttpResponseRedirect('/login/')



def viewthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']

				hist=[]

				try:
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)
					thriftrec=tblthrift.objects.filter(customer=details).order_by('id').reverse()
					for k in thriftrec:
						tdate= int(k.number)
						month = k.month
						df={'month':month,'thrift':k.thrift}
						hist.append(df)

					return render_to_response('thrift/mythrifthistory.html',{'company':mybranch,'user':varuser,
							'hist':hist,'details':details,'wallet':mywallet})
				
				except:
					msg = 'invalide wallet address'
					return render_to_response('thrift/viewthrifthistory.html',{'company':mybranch,'user':varuser,'form':form,'msg':msg})
		else:
			form=viewwalletform()
		return render_to_response('thrift/viewthrifthistory.html',{'company':mybranch,'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')

def changethrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
			
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		dattee= date.today().month
		
		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']

				try:
					details=tblCUSTOMER.objects.get(merchant=memmerchant,wallet=mywallet,status=1)
					myform = thriftform()
				except:
					msg = 'invalide wallet address'
					return render_to_response('thrift/changethrift.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
				try:
					thrift=tblthrift.objects.get(customer=details,number = dattee)
				except:
					msg ='NO THRIFT RECORD FOUND'
					return render_to_response('thrift/changethrift.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

				thriftrec = tblthrift_trans.objects.filter(customer=details,recdate__month = dattee)

				return render_to_response('thrift/mychangethistory.html',{'company':mybranch, 'user':varuser,'form':myform,
						'wallet':mywallet,'thrift':thrift,'thriftrec':thriftrec,'date':dattee})

		else:
			form=viewwalletform()
		return render_to_response('thrift/changethrift.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')



def thriftedit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		dattee= date.today().month
		

		if request.method == 'POST':
			mywallet=request.POST['wallet']
			ttr=request.POST['thrift']
			dd=request.POST['date'] #month in fnumber
			dd = calendar.month_name[int(dd)] #converts to month name

			return render_to_response('thrift/prevchan.html',{'company':mybranch, 'user':varuser,'month':dd,'wallet':mywallet,'thrift':ttr})

	else:
		return HttpResponseRedirect('/login/')


def safethriftedit(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		dattee= date.today().month
		

		if request.method == 'POST':
			mywallet=request.POST['wallet']
			ttr=request.POST['thrift']
			dd=request.POST['month'] #month in words
			newthrift = request.POST['newt']

			if newthrift !='':
				customer=tblCUSTOMER.objects.get(wallet=mywallet,status=1)
				firstthrift = tblthrift.objects.get(month=dd,customer=customer)
				firstthrift.thrift=newthrift
				firstthrift.save()
				return render_to_response('thrift/savethriftsuccess.html',{'company':mybranch, 'user':varuser,'month':dd,'wallet':mywallet,'thrift':ttr,'newt':newthrift})
			else:
				return HttpResponseRedirect('/thrift/thrift/changethrift/')
	else:
		return HttpResponseRedirect('/login/')


def rolloverthrift(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		
		mydatee=date.today().month #month in figures
		current_date =int(mydatee)
		yday = date.today().year
		ddt= calendar.month_name[int(mydatee)] #month in words

		if mydatee == 12:
			nextmonth = 1
			yday=yday+1
		else:
			nextmonth=mydatee + 1

		nnm= calendar.month_name[int(nextmonth)]

		if request.method=='POST':
			details=tblCUSTOMER.objects.filter(branch=mybranch, merchant=memmerchant,status=1)
			for  k in details:
				try:
					thriftrec=tblthrift.objects.get(customer=k,number=mydatee)							
					
					if tblthrift.objects.filter(customer=k,merchant=memmerchant,branch=mybranch,year =yday, month=nnm, number=nextmonth).count() == 0:
						tblthrift(customer=k,merchant=memmerchant,branch=mybranch,year =yday, month=nnm,thrift=thriftrec.thrift,code = 87867, number=nextmonth).save()
			
				except:

					if tblthrift.objects.filter(customer=k,merchant=memmerchant,branch=mybranch,year =yday, month=nnm,number=nextmonth).count()==0:
						tblthrift(customer=k,merchant=memmerchant,branch=mybranch,year =yday, month=nnm,thrift=0,code = 87867, number=nextmonth).save()
			return render_to_response('thrift/rollsuccess.html',{'company':mybranch, 'user':varuser,'month':ddt,'nextmonth':nnm})

		else:
			return render_to_response('thrift/rolloverthrift.html',{'company':mybranch, 'user':varuser,'month':ddt,'nextmonth':nnm})

	else:
		return HttpResponseRedirect('/login/')




####  CAsh iN prOcedures************************

def payrequests(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
					
		mydate=date.today().month #gives month in number
		month= calendar.month_name[mydate] #converts month number to month name
		datee= date.today()

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(wallet=mywallet,status=1,
							merchant=memmerchant,branch=mybranch)
					jk = tblthrift_trans.objects.filter(customer=details,recdate__month=mydate)
					add=jk.aggregate(Sum('number'))
					add = add['number__sum']

				except:
					msg = 'invalide wallet address or you are not the merchant for this customer'
					return render_to_response('thrift/payrequest.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

				myform = thriftamountform()
				try:
					rele= tblthrift.objects.get(number=mydate,customer=details)
					mythrift=rele.thrift
					thriftrec=tblthrift.objects.get(customer=details,number=mydate)				
				except:
					msg = 'thrift details not found for this month'
					return render_to_response('thrift/nothrift.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg,'wallet':mywallet})
					
				return render_to_response('thrift/paythrift.html',{'company':mybranch,'date':datee,
					'month':month,'thrift':mythrift,'user':varuser,
					'form':myform,'number':add,
					'wallet':mywallet,'thriftrec':thriftrec})
			else:
				pass
		else:
			form=viewwalletform()
		return render_to_response('thrift/payrequest.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')

def source(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		acccode,wallet,thrift,month=acccode.split(':')
    		if acccode== '-----': 
    			return render_to_response('thrift/selectloan.html')
    		elif acccode=='Cash': 
    			myform = thriftamountform()
    			return render_to_response('thrift/cash.html',{'form':myform,
    				'wallet':wallet,'thrift':thrift,'month':month})
    		elif acccode=='Transfer':
    			return render_to_response('thrift/transfer.html')

    		return render_to_response('thrift/remtrans.html',{'income':mycom,'date1':trandate})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')




def json_view(func):
    def wrap(req, *args, **kwargs):
        resp = func(req, *args, **kwargs)
        if isinstance(resp, HttpResponse):
            return resp
        return HttpResponse(json.dumps(resp), mimetype="application/json")

    return wrap

@json_view
def autocomplete(request):
    term = request.GET.get('term')

	# varuser=request.session['userid']
	# staff = Userprofile.objects.get(email=varuser,status=1)

	# if staff.thrift==0:
	# 	return render_to_response('404.html',{'company':mybranch, 'user':varuser})

	# staffdet=staff.staffrec.id
	# branch=staff.branch.id

	# mycompany=staff.branch.company
	# company=mycompany.name
	# comp_code=mycompany.id
	# ourcompay=tblCOMPANY.objects.get(id=comp_code)

	# mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

	# memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)


    
    suggestions = []
    qset = tblthrift.objects.get(code =8797)#[:10]
    thrift  = 1000
    thrr = 2000
    suggestions.append(thrr)
    
    # for x in range(1,6): 
    # 	thrr = x * thrift
    # 	suggestions.append({'label': '%s :%s :%s :%s ' % (x, thrr), 'number': x,'amount':thrr})
    # 	# suggestions.append({'amount':thrr})
    return suggestions

    # for i in qset:
    #     suggestions.append({'label': '%s :%s :%s :%s ' % (i.admissionno, i.fullname,i.admitted_class,i.admitted_arm), 'admno': i.admissionno,'name':i.fullname,'klass':i.admitted_class,'arm':i.admitted_arm})
    # return suggestions



def history(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		mydate=date.today().month
		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(merchant=memmerchant, wallet=mywallet,status=1)
					thriftrec= tblthrift_trans.objects.filter(customer=details, reason='Available').order_by('recdate').reverse()

					add=thriftrec.aggregate(Sum('amount'))
					add = add['amount__sum']

					return render_to_response('thrift/conthistory.html',{'customer':details,'user':varuser,
					'wallet':mywallet,'thriftrec':thriftrec,'bal':add})
					
				except:
					msg = 'invalide wallet address'
					return render_to_response('thrift/payhistory.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

		else:
			form=viewwalletform()

		return render_to_response('thrift/payhistory.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')



def cashin(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		if staff.thrift==0: 
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
	
		if request.method == 'POST':
			form = thriftamountform(request.POST)
			if form.is_valid():
				amount=form.cleaned_data['amount']
				mythrift=request.POST['thrift']
				wallet=request.POST['wallet']
				amount=int(amount)
				mythrift=int(mythrift)

				k,l=divmod(amount,mythrift)
							
				todays=date.today()
				weekday=date.today().isocalendar()[1]

### working out week number for the year, for the date
				
				
				if l == 0:
					k = random.randint(0,9)
					y = random.randint(0,9)
					x = random.randint(0,9)
					z = random.randint(0,9)
					a = random.randint(0,9)
					pin =  str(k) + str(y) + str(x) + str(z)+ str(a)

					customer=tblCUSTOMER.objects.get(wallet=wallet,status=1,merchant=memmerchant,branch=mybranch)
					countt= tblMerchantTrans.objects.filter(branch=mybranch,customer=customer,
						merchant=memmerchant,recdate=todays,amount=amount,types='Main',
						remitted='Unremmitted', approved='Not Approved').count()
					
					if countt<1:
						tblMerchantTrans(weekno=weekday, branch=mybranch,customer=customer,merchant=memmerchant,recdate=todays,amount=amount,types='Main',remitted='Unremmitted', approved='Not Approved',code=pin).save()
						return render_to_response('thrift/cashinthriftsuccess.html',{'company':mybranch, 'user':varuser,'wallet':wallet,'thrift':mythrift,'amount':amount})
					else:
						msg ='YOU CANNOT POST SAME AMOUNT TWICE, SAME DAY'
				else:
					return HttpResponseRedirect('/login/')

		else:
			form=viewwalletform()
			msg = ''
		return render_to_response('thrift/payrequest.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/')

def unremmitted(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		
		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form = viewallremittedform(request.POST)
			if form.is_valid():
				mystatus=form.cleaned_data['status']
				tdate=form.cleaned_data['date']

				yday,mday,dday = tdate.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				oydate=date(yday,mday,dday)

				# thismonth= calendar.month_name[mday]

				thriftrec=[]

				# thismonth= calendar.month_name[mday]
				# month_name = calendar.month_abbr[2]
				# month_number = list(calendar.month_abbr).index('Feb')


				if mystatus == '---' or tdate == '---':
					return HttpResponseRedirect('/thrift/thrift/unremmitted/')
				
				elif mystatus=='Remitted':				

					trec=tblmerchantBank.objects.filter(merchant=memmerchant,branch=mybranch,
						recdate=oydate,
						# status=mystatus
						)

				elif mystatus=='Unremmitted':
					trec = tblMerchantTrans.objects.filter(branch=mybranch,merchant=memmerchant,
						types='Main',recdate=oydate,remitted=mystatus)
					
				else:
					trec=tblmerchantBank.objects.filter(merchant=memmerchant,branch=mybranch,
						recdate=oydate,)


					trec = tblMerchantTrans.objects.filter(branch=mybranch,merchant=memmerchant,
						types='Main',recdate=oydate,remitted=mystatus)

				countt=trec.count()

				if countt>0:
					add=trec.aggregate(Sum('amount'))
					add = add['amount__sum']
					dl={'amount':add,'date':oydate}
					thriftrec.append(dl)

				else:
					add=trec.aggregate(Sum('amount'))
					add = add['amount__sum']
					dl={'amount':0,'date':oydate}
					thriftrec.append(dl)

				return render_to_response('thrift/merchantpayhistory.html',{'company':mybranch, 'user':varuser,'thriftrec':thriftrec,'status':mystatus})
			


				msg = 'invalide Details'
				return render_to_response('thrift/payrequest.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

		else:
			form=viewallremittedform()
			# form=unremitform()
		return render_to_response('thrift/unremmitted.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')

def cashout(request):
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

		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = withcashform(request.POST)
			if form.is_valid():
				wallet=form.cleaned_data['wallet']
				tdate=form.cleaned_data['date']

				yday,mday,dday = tdate.split('/') #JSON Dates Object
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				thismonth= calendar.month_name[mday]
				dll = []	

				try:
					customer=tblCUSTOMER.objects.get(merchant=memmerchant,wallet=wallet,status=1)

					paydetail=tblthrift_trans.objects.filter(merchant=memmerchant,branch=mybranch,recdate__month=mday,
						customer=customer,types='Main',avalability="Available",reason="Available")

					cus_thrift=tblthrift.objects.get(branch=mybranch,merchant=memmerchant,
						customer=customer,number = mday)
					cus_thrift=cus_thrift.thrift

					for d in paydetail:
						avalability=d.avalability
						add=paydetail.aggregate(Sum('amount'))
						add = add['amount__sum']
						num=paydetail.aggregate(Sum('number'))

						num = num['number__sum']
						jdjd= {'thrift':cus_thrift, 'amount':add,'num':num,'status':avalability,'month':thismonth}
					dll.append(jdjd)

	

					return render_to_response('thrift/reqcash.html',{'thriftrec':dll,'company':mybranch,
						'user':varuser,'wallet':wallet,
						'month':thismonth,
						'date':tdate,'year':yday})
				


				except:
					msg="Records not found"
				return render_to_response('thrift/cashout.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

		else:
			form=withcashform()
		return render_to_response('thrift/cashout.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')

def cashoutrequest(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		
		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
			

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		try:
			memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		except:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			wallet=request.POST['wallet']
			datet =request.POST['date']

			myydate = date.today()

			yday,mday,dday = datet.split('/') #JSON Dates Object
			yday=int(yday)
			mday=int(mday)
			ddd=int(dday)

			weeknos=date.today().isocalendar()[1]
			month=calendar.month_name[mday]
				
			customer=tblCUSTOMER.objects.get(merchant=memmerchant,wallet=wallet,status=1)
			
			paydetail=tblthrift_trans.objects.filter(merchant=memmerchant,branch=mybranch,recdate__month=mday,
				customer=customer,types='Main',avalability="Available",reason="Available")

			for d in paydetail:
				code = d.code
				amount=d.amount
				try:
					tblpayoutrequest.objects.get(weekno=weeknos, branch=mybranch,merchant=memmerchant,customer=customer,
						date=myydate,status='Unpaid',amount=amount,month=month)

				except:
					tblpayoutrequest(weekno=weeknos,branch=mybranch,merchant=memmerchant,customer=customer,
						date=myydate,status='Unpaid',amount=amount,
						month=month,code=code).save()
					
					#d.delete()
					d.reason='Requsted'
					d.save()

			return render_to_response('thrift/payoutsuccess.html',{'company':mybranch, 'user':varuser,'thriftrec':paydetail})#'tot':total})
	
	else:
		return HttpResponseRedirect('/login/')

def individual(request):
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
			form = remittalform(request.POST)
			if form.is_valid():
				merchant =form.cleaned_data['merchant']
				mydate2=form.cleaned_data['date']  #JavaScript Date Object

				yday,mday,dday = mydate2.split('/') 
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday) #Python Date Object

        		try:
        		    memmerchant=tblMERCHANT.objects.get(id=merchant,status=1,branch=mybranch)
        		except:
        		    form=remittalform()
        		    msg = 'INVALID MERCHANT ID'
        		    return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
        		ddt=[]
        		thriftrec= tblMerchantTrans.objects.filter(branch=mybranch,merchant=merchant,
					recdate=mydate,types='Main',remitted='Unremmitted',approved='Not Approved')

        		mycount= thriftrec.count()

        		if mycount >0:
        			add=thriftrec.aggregate(Sum('amount'))
        			add = add['amount__sum']
        			dl={'amount':add}
        			ddt.append(dl)
        			return render_to_response('thrift/remhistory.html',{'company':mybranch,'dates':mydate2, 
        				'merchant':merchant,'user':varuser,'thriftrec':ddt,'date':mydate,'ttt':thriftrec})
        		
        		else:
        			msg ='NO TRANSACTION FOUND'
		else:
			form=remittalform()
			msg=''
		return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')


def reedit(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		merchant,trandate=acccode.split(':')

        	yday,mday,dday = trandate.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)
        	mydatwwwe=date(yday,mday,dday)

        	merchant1=tblMERCHANT.objects.get(id=merchant,status=1)
        	mybranch=merchant1.branch.id

    		ddt=[]

    		thriftrec= tblMerchantTrans.objects.filter(branch=mybranch,merchant=merchant1,
				recdate=mydatwwwe,types='Main',remitted='Unremmitted',approved='Not Approved')

    		mycount= thriftrec.count()

    		if mycount >0:
    			add=thriftrec.aggregate(Sum('amount'))
    			add = add['amount__sum']
    			dl={'amount':add}
    			ddt.append(dl)
    			return render_to_response('thrift/remall.html',{'company':mybranch,'dates':trandate, 
    				'merchant':merchant,'thriftrec':ddt,'date':mydatwwwe,'ttt':thriftrec})
  
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')

def seedit(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate=acccode.split(':')

    		try: 

	    		mymy = tblMerchantTrans.objects.get(id=state)
	    		cid =mymy.customer.id
	    		
	    		jjf= tblCUSTOMER.objects.get(id=cid,status=1)

	        	yday,mday,dday = trandate.split('/')
	        	yday=int(yday)
	        	mday=int(mday)
	        	dday=int(dday)
	        	mydatwwwe=date(yday,mday,dday)

	    		mycom = tblMerchantTrans.objects.get(customer=jjf,recdate=mydatwwwe,id=state )

	    		return render_to_response('thrift/remtrans.html',{'income':mycom,'date1':trandate})

    		except : 
    			return HttpResponseRedirect('/thrift/thrift/remittals/')

    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')


def indremitcash(request):
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

        if staff.cashier==0:
        	return render_to_response('404.html',{'company':mybranch, 'user':varuser})
        
     
        if request.method == 'POST':
        	merchant=request.POST['merchant']
        	transid = request.POST['trans']
        	cash =request.POST['cash'] #posted
        	mmm =request.POST['mmm'] #carry come
        	mydate2=request.POST['date1'] #Javascript date object

        	yday,mday,dday = mydate2.split('/')
        	yday=int(yday)
        	mday=int(mday)
        	dday=int(dday)

        	mydate=date(yday,mday,dday) #python date object

        	fdate= datetime.today()
        	remterr=date(fdate.year,fdate.month,fdate.day)
        	
        	weekday=remterr.isocalendar()[1]

        	ddt5=[]

        	merchanttt=tblMERCHANT.objects.get(id=merchant,status=1)
        	msid=merchanttt.staff.id
        	msid=tblSTAFF.objects.get(id=msid)

        	if mmm == cash: 

        		try: 

		    		mymy = tblMerchantTrans.objects.get(id=transid)
		    		cid =mymy.customer.id
		    		
		    		jjf= tblCUSTOMER.objects.get(id=cid,status=1)

	        		mycom = tblMerchantTrans.objects.get(customer=jjf,recdate=mydate,id=transid)
	        		code=mycom.code

	        		try:
	        			tblmerchantBank.objects.get(branch=mybranch,recdate=mydate,
	        				amount=cash,status='Remitted',customer = jjf,
	        				weekno=weekday,merchant=merchanttt,code=code)

	        		except:
	        			tblmerchantBank(branch=mybranch,recdate=mydate,
	        				amount=cash,staffrec= msid,status='Remitted', 
	        				remitted_by = varuser,customer = jjf,weekno=weekday,
	        				merchant=merchanttt,code=code,rem_date=remterr).save()
	        			mycom.delete()
	        
	        		thriftrec= tblMerchantTrans.objects.filter(branch=mybranch,merchant=merchanttt,recdate=mydate,types='Main',remitted='Unremmitted',approved='Not Approved')
	        		mycount= thriftrec.count()

	        		if mycount >0:
	        			add=thriftrec.aggregate(Sum('amount'))
	        			add = add['amount__sum']
	        			dl={'amount':add}
	        			ddt5.append(dl)
	        			return render_to_response('thrift/remhistory.html',{'company':mybranch,'dates':mydate2,'date':mydate,'merchant':merchant,'user':varuser,'thriftrec':ddt5,'ttt':thriftrec})



        	
        		except:

        			return HttpResponseRedirect('/thrift/thrift/remittals/')



        		else:
        			return render_to_response('thrift/remsuccess_indiv.html',{'company':mybranch, 'cdate':mydate2,'merchant':merchant,'user':varuser,'total':cash})
        	else:
        		msg = "YOU ENTERED A WRONG FIGURE"
        		return HttpResponseRedirect("/thrift/thrift/remittals/")
        		# jk='op'  #close the pop up and do nothing

        else:
        	return HttpResponseRedirect('/login/')

    else:
        return HttpResponseRedirect('/login/')






def remitcash(request):
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

        if staff.cashier==0:
        	return render_to_response('404.html',{'company':mybranch, 'user':varuser})
     
        if request.method == 'POST':
            merchant1 =request.POST['merchant']
            mydate1=request.POST['dates']
            cashe1=request.POST['cash']
            amount= request.POST['amount']

            yday,mday,dday = mydate1.split('/')
            yday=int(yday)
            mday=int(mday)
            dday=int(dday)

            fdate= datetime.today()
            remdate=date(fdate.year,fdate.month,fdate.day)



            mydate=date(yday,mday,dday)
            weekday=date(yday,mday,dday).isocalendar()[1]   #week no of date         
            ddt=[]

            merchant=tblMERCHANT.objects.get(id=merchant1,status=1)
            stafff=merchant.staff.id
            memstaff = tblSTAFF.objects.get(branch=mybranch,id=stafff)

            if cashe1 == amount:
            	thriftrec= tblMerchantTrans.objects.filter(branch=mybranch,merchant=merchant,recdate=mydate,types='Main',remitted='Unremmitted',approved='Not Approved')

            	for k in thriftrec:
            		code=k.code
            		try:
            			tblmerchantBank.objects.get(branch=mybranch,recdate=mydate,amount=k.amount,customer = customer, status='Remitted', merchant=merchant,code=code)
            		except:
            			customer=k.customer.id
            			customer=tblCUSTOMER.objects.get(id=customer,status=1)
            			tblmerchantBank(weekno=weekday,branch=mybranch,
            				recdate=mydate,amount=k.amount,staffrec= memstaff,
            				status='Remitted', remitted_by = varuser,rem_date=remdate,
            				customer = customer, merchant=merchant,code=code).save()
            			k.delete()
            	return render_to_response('thrift/remsuccess.html',{'company':mybranch,'merchant':merchant1,'cdate':mydate1, 'user':varuser,'total':cashe1})

            else:
            	return HttpResponseRedirect('/thrift/thrift/remittals/')
        else:
            form=remittalform()
        return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form})
        
    else:
        return HttpResponseRedirect('/login/')


def approveind(request):
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
		
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			merchant =request.POST['merchant']
			mydate2=request.POST['cdate']  #JavaScript Date Object
			cid = request.POST['customer_id']
			amount=request.POST['total']

			yday,mday,dday = mydate2.split('/') 
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #Python Date Object
			customer= tblCUSTOMER.objects.get(id =cid,status=1)
			customer1=customer.id
			mymerchant= tblMERCHANT.objects.get(id=merchant,status=1)

			myadmin = tblmerchantBank.objects.get(remitted_by=varuser, status='Remitted',branch=mybranch,customer=customer,
				amount=amount,recdate=mydate,merchant=mymerchant)
			add =myadmin.amount
			remtotal=myadmin.amount
		
			return render_to_response('thrift/approvalindv.html',{'company':mybranch,'merchant':merchant,'customer':customer1,
				'user':varuser,'date':mydate,'thriftrec':myadmin,'cdate':mydate2,'total':add,'rem':remtotal})

	else:
		return HttpResponseRedirect('/logout/')


def approveindividualcash(request):
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

     	if staff.admin==0:
    		return render_to_response('404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
            merchant =request.POST['merchant']
            mydate=request.POST['date']
            customer=request.POST['customer'] #already a database instance

            yday,mday,dday = mydate.split('/')

            yday=int(yday)
            mday=int(mday)
            dday=int(dday)

            transdate=date(yday,mday,dday)
            ddt=[]

            merchant=tblMERCHANT.objects.get(status=1,id=merchant)
         
            remit = tblmerchantBank.objects.filter(branch=mybranch,merchant=merchant,recdate = transdate,status='Remitted',customer=customer)
            
            count=remit.count()

            for k in remit:
            	code=k.code
                customer=k.customer.id
                customer=tblCUSTOMER.objects.get(id=customer,status=1)
                
                mythrift=tblthrift.objects.get(branch=mybranch,
                	customer=customer,number=mday,year=yday)

                customer_thrift = mythrift.thrift
                number= k.amount / customer_thrift
                pl= number-1
                new_amount = k.amount - customer_thrift
                
                mont_contribution = tblthrift_trans.objects.filter(branch=mybranch,merchant=merchant,
                    customer=customer,recdate__month=mday,types='Main').count()
                
                if mont_contribution<1:                    
                    if number == 1:
                        tblthrift_trans(branch=mybranch,code=code,merchant=merchant,customer=k.customer,
                            number=1,recdate=transdate,amount=customer_thrift,types='Main',
                            avalability='Not Available',reason='Account Maintenance').save()
                        k.status='Approved'
                        k.approved_by=varuser
                        k.save()

                    elif number > 1:
                        tblthrift_trans(branch=mybranch,merchant=merchant,code=code,customer=k.customer,
                            number=1,recdate=transdate,amount=customer_thrift,types='Main',
                            avalability='Not Available',reason='Account Maintenance').save()
                        
                        tblthrift_trans(branch=mybranch,merchant=merchant,code=code,customer=k.customer,
                            number=pl,recdate=transdate,amount=new_amount,types='Main',
                            avalability='Available',reason='Available').save()
                        k.status='Approved'
                        k.approved_by=varuser
                        k.save()

                else:
                    tblthrift_trans(branch=mybranch,merchant=merchant,customer=k.customer,
                        number=number,recdate=transdate,amount=k.amount,code=code,
                        types='Main',avalability='Available',reason='Available').save()
                    k.status='Approved'
                    k.approved_by=varuser
                    k.save()
				
            return render_to_response('thrift/approve_success.html',{'company':mybranch,'tot':count,'user':varuser})

        else:
            form=remittalform()
        return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form})
        
    else:
        return HttpResponseRedirect('/login/')




def remitcash_old(request):
    if 'userid' in request.session:
        varuser=request.session['userid']
        staff = Userprofile.objects.get(email=varuser,status=1)
        
        if staff.cashier==0:
        	return render_to_response('404.html',{'company':mybranch, 'user':varuser})
            
        staffdet=staff.staffrec.id
        branch=staff.branch.id
        mycompany=staff.branch.company
        company=mycompany.name
        comp_code=mycompany.id
        ourcompay=tblCOMPANY.objects.get(id=comp_code)

        mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
        memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
     
        if request.method == 'POST':
            merchant1 =request.POST['merchant']
            mydate1=request.POST['dates']
            cashe1=request.POST['cash']

            yday,mday,dday = mydate1.split('/')
            yday=int(yday)
            mday=int(mday)
            dday=int(dday)
            mydate=date(yday,mday,dday)

            fdate= datetime.today()
            remterr=date(fdate.year,fdate.month,fdate.day)

            weekday=date(yday,mday,dday).isocalendar()[1]   #week no of date         
            ddt=[]

            merchant=tblMERCHANT.objects.get(id=merchant1,status=1)
            stafff=merchant.staff.id
            memstaff = tblSTAFF.objects.get(branch=mybranch,id=stafff)

            thriftrec= tblMerchantTrans.objects.filter(branch=mybranch,merchant=merchant,
                recdate=mydate,types='Main',remitted='Unremmitted',approved='Not Approved')

            for k in thriftrec:
                try:
                    tblmerchantBank.objects.get(branch=mybranch,recdate=mydate,amount=k.amount,
                    	customer = customer, status='Remitted', merchant=merchant,code=36374)
                except:
                	customer=k.customer.id
                	customer=tblCUSTOMER.objects.get(id=customer,status=1)
                	tblmerchantBank(weekno=weekday,branch=mybranch,
                		recdate=mydate,amount=k.amount,
                		staffrec= memstaff,status='Remitted',
                		remitted_by = varuser, customer = customer,
                		merchant=merchant,code=36374,rem_date=remterr).save()
                	k.delete()
            return render_to_response('thrift/remsuccess.html',{'company':mybranch,'merchant':merchant1,'cdate':mydate1, 'user':varuser,'total':cashe1})

        else:
            form=remittalform()
        return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form})
        
    else:
        return HttpResponseRedirect('/login/')



def all(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		
		staff=Userprofile.objects.get(email=varuser,status=1)
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
			# return render_to_response('404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)


## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		memmerchant=tblMERCHANT.objects.filter(staff=memstaff,status=1)

		if request.method == 'POST':
			form = viewremallform(request.POST)
			if form.is_valid():
				# checkbox =request.POST['checkbox']
				mydate=form.cleaned_data['date']
				yday,mday,dday = mydate.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				ddt=[]

				ddd= dday+1

				for d in xrange(ddd):
					if d == 0:
						pass
					else:
						mydate= date(yday,mday,d)

						for merchant in memmerchant:
							thrifing= tblMerchantTrans.objects.filter(branch=mybranch,
								recdate=mydate,types='Main',remitted='Unremmitted',merchant=merchant)
							
							mycount= thrifing.count()

							if mycount >0:
								add=thrifing.aggregate(Sum('amount'))
								add = add['amount__sum']
								dl={'date':mydate,'amount':add,'merchant':merchant,'remitted':'Unremmitted'}
								ddt.append(dl)
							else:
								pass

				return render_to_response('thrift/allrem.html',{'company':mybranch, 'user':varuser,'thriftrec':ddt,'date':mydate})

		else:
			form=viewremallform()
		return render_to_response('thrift/all.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')


def report(request):
	if 'userid' in request.session:
		varuser=request.session['userid']		
		staff=Userprofile.objects.get(email=varuser,status=1)

		staffdet=staff.staffrec.id
		branch=staff.branch.id

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.cashier==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewallremittedform(request.POST)
			if form.is_valid():
				status=form.cleaned_data['status']
				date1=form.cleaned_data['date']
				yday,mday,dday = date1.split('/')

				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday)
				month = calendar.month_name[mday]
								
				allmerchant = tblMERCHANT.objects.filter(branch=mybranch,status=1)
				remm=[]
				all_data=[]

				if 'checkbox' in request.POST:
					checkbox=request.POST['checkbox']
				else:
					checkbox=1
				
				if checkbox==1:
					if status == 'Remitted':						
						for k in allmerchant:
							thriftrec= tblmerchantBank.objects.filter(branch=mybranch,recdate=mydate,merchant=k)
							add=0
							add = thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']
							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)

					elif status == 'Unremmitted':
						for p in allmerchant:
							thriftrec= tblMerchantTrans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=mydate,merchant=p)
							add =0
							
							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':p,'amount':add}
								remm.append(gh)
						
					return render_to_response('thrift/remreport.html',{'company':mybranch,'user':varuser,
						'thriftrec':remm,'date':mydate,'status':status})

				else: # if checkbox == month


					P = (monthrange(yday, mday))[-1]
					for n in range (P,0,-1):		
						realdate = date(yday,mday,n)
						k =0
						if status=='Remitted':
							for mn in allmerchant:								
								thriftrec= tblmerchantBank.objects.filter(branch=mybranch,recdate=realdate,merchant=mn)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':mn,'amount':add,'month':realdate}
									remm.append(gh)

							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

						elif status == 'Unremmitted':
							for kl in allmerchant:
								thriftrec= tblMerchantTrans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=realdate,merchant=kl)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':kl,'amount':add,'month':realdate}
									remm.append(gh)
							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

					return render_to_response('thrift/histremreport.html',{'company':mybranch, 'user':varuser,
						'thriftrec':all_data,'month':month,'year':yday,'status':status})
		
		else:
			form=viewallremittedform()
		return render_to_response('thrift/report.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')



def approvalsmenu(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		msg=''

		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewmerchantform(request.POST)
			if form.is_valid():
				merchant2=form.cleaned_data['merchant']
				mydate=form.cleaned_data['date']

				yday,mday,dday=mydate.split('/')
				yday=int(yday)
				mday=int(mday)
				dday=int(dday)

				memmerchant=tblMERCHANT.objects.get(id=merchant2, status=1)

				transdate=date(yday,mday,dday)

				remit = tblmerchantBank.objects.filter(branch=mybranch,merchant=memmerchant,recdate = transdate, status='Remitted')

				remamount = tblmerchantBank.objects.filter(branch=mybranch,recdate=transdate,merchant=merchant2,status='Remitted')


				count=remit.count()
				ggt=[]

				if count>0:
					for k in remit:
						name=k.customer.surname + "   "+k.customer.firstname
						customer=k.customer.id
						customer=tblCUSTOMER.objects.get(id=customer,status=1)
						cus_thrift = tblthrift.objects.get(customer=customer,merchant=memmerchant,number = mday,year=yday)
						cus_thrift=cus_thrift.thrift
						df={'thrift':cus_thrift,'amount':k.amount,'name':name,'status':'Not Approved'}
						ggt.append(df)

					add=remit.aggregate(Sum('amount'))
					add = add['amount__sum']
					add = int(add)


					remtotal=remamount.aggregate(Sum('amount'))
					remtotal = remtotal['amount__sum']
					remtotal = int(remtotal)
				
					return render_to_response('thrift/approvalhistory.html',{'company':mybranch,'merchant':merchant2,
						'user':varuser,'date':transdate,'thriftrec':ggt,'cdate':mydate,'total':add,'rem':remtotal})
				else:
					
					return render_to_response('thrift/nilem.html',{'company':mybranch, 'user':varuser,'form':form})
		else:
			form=viewmerchantform()
		return render_to_response('thrift/approvalsmenu.html',{'company':mybranch, 'user':varuser,'form':form,'msg':msg})
		
	else:
		return HttpResponseRedirect('/login/')


def approvecash(request):
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

     	if staff.admin==0:
    		return render_to_response('404.html',{'company':mybranch, 'user':varuser})

        if request.method == 'POST':
            merchant =request.POST['merchant']
            mydate=request.POST['date'] #JS date object

            yday,mday,dday = mydate.split('/')

            yday=int(yday)
            mday=int(mday)
            dday=int(dday)

            transdate=date(yday,mday,dday) #python date object
            ddt=[]

            merchant=tblMERCHANT.objects.get(status=1,id=merchant)

            remit = tblmerchantBank.objects.filter(branch=mybranch,merchant=merchant,recdate = transdate,status='Remitted')
            
            count=remit.count()

            for k in remit:
            	code=k.code
                customer=k.customer.id
                customer=tblCUSTOMER.objects.get(id=customer,status=1)
                
                mythrift=tblthrift.objects.get(branch=mybranch,
                	customer=customer, number = mday,year=yday)

                customer_thrift = mythrift.thrift
                number= k.amount / customer_thrift
                pl= number-1
                new_amount = k.amount - customer_thrift

  #take note of this               
                mont_contribution = tblthrift_trans.objects.filter(branch=mybranch,merchant=merchant,
                    customer=customer,recdate__month=mday,types='Main').count() 
                

                if mont_contribution<1:
                    if number == 1:
                        tblthrift_trans(branch=mybranch,merchant=merchant,code=code,customer=customer,
                            number=1,recdate=transdate,amount=customer_thrift,types='Main',
                            avalability='Not Available',reason='Account Maintenance').save()
                        k.status='Approved'
                        k.approved_by=varuser
                        k.save()

                    elif number > 1:
                        tblthrift_trans(branch=mybranch,merchant=merchant,customer=customer,
                            code=code,number=1,recdate=transdate,amount=customer_thrift,types='Main',
                            avalability='Not Available',reason='Account Maintenance').save()
                        
                        tblthrift_trans(branch=mybranch,merchant=merchant,customer=k.customer,
                            number=pl,code=code,recdate=transdate,amount=new_amount,types='Main',
                            avalability='Available',reason='Available').save()
                        k.status='Approved'
                        k.approved_by=varuser
                        k.save()

                else:
                    tblthrift_trans(branch=mybranch,merchant=merchant,customer=k.customer,
                        code=code,number=number,recdate=transdate,amount=k.amount,
                        types='Main',avalability='Available',reason='Available').save()
                    k.status='Approved'
                    k.approved_by=varuser
                    k.save()
				
            return render_to_response('thrift/approve_success.html',{'company':mybranch,'tot':count,'user':varuser})

        else:
            form=remittalform()
        return render_to_response('thrift/remittals.html',{'company':mybranch, 'user':varuser,'form':form})
        
    else:
        return HttpResponseRedirect('/login/')


def allapproval(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
			# return render_to_response('404.html')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)

		if request.method == 'POST':
			form = viewallremittedform(request.POST)
			merchant =request.POST['merchant']
			mydate=request.POST['date']
			yday,mday,dday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			transdate=date(yday,mday,dday)
		else:
			form=viewallremittedform()
		return render_to_response('thrift/allapproval.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/')



def approvereport(request):
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

		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})


		if request.method == 'POST':
			form  = form=viewallapprovedform(request.POST)
			status =request.POST['status']
			mydate=request.POST['date'] #javascript date object
			yday,mday,dday = mydate.split('/')
			yday=int(yday)
			mday=int(mday)
			dday=int(dday)
			mydate=date(yday,mday,dday) #python date object
			realmonth=calendar.month_name[mday]
	
			allmerchant = tblMERCHANT.objects.filter(branch=mybranch,status=1)
			remm=[]
			all_data=[]

			if 'checkbox'  in request.POST:
				checkbox=request.POST['checkbox']
			else:
				checkbox=1

			if checkbox==1:
				if status=="Approved":
					for k in allmerchant:
						thriftrec= tblmerchantBank.objects.filter(status=status, branch=mybranch,recdate=mydate,merchant=k)
						
						add=thriftrec.aggregate(Sum('amount'))
						add = add['amount__sum']

						if add > 0:
							gh={'my_merchant':k,'amount':add}
							remm.append(gh)

				elif status=="Not Approved":

					for k in allmerchant:
						thriftrec= tblmerchantBank.objects.filter(status='Remitted', branch=mybranch,recdate=mydate,merchant=k)
						
						add=thriftrec.aggregate(Sum('amount'))
						add = add['amount__sum']

						if add > 0:
							gh={'my_merchant':k,'amount':add}
							remm.append(gh)
					
				return render_to_response('thrift/appreport.html',{'company':mybranch, 'user':varuser,
					'thriftrec':remm,'date':mydate,'status':status})


			else:
				P = (monthrange(yday, mday))[-1]
				for n in range (P,0,-1):
					realdate = date(yday,mday,n)
					k =0
					if status=="Not Approved":
						for kp in allmerchant:
							thriftrec= tblmerchantBank.objects.filter(status='Remitted', branch=mybranch,recdate=realdate,merchant=kp)			
							if thriftrec.count() > 0:
								k = 'fff'
								add=thriftrec.aggregate(Sum('amount'))
								add = add['amount__sum']
								gh={'my_merchant':kp,'amount':add,'date':realdate}
								remm.append(gh)
						if k =='fff':
							datasdict={'remm':remm,'udate':realdate}
							all_data.append(datasdict)				
				
					elif status=="Approved":
						for kpo in allmerchant:								
							thriftrec= tblmerchantBank.objects.filter(status=status, branch=mybranch,recdate=realdate,merchant=kpo)
							if thriftrec.count() > 0:
								k = 'fff'
								add=thriftrec.aggregate(Sum('amount'))
								add = add['amount__sum']
								gh={'my_merchant':kpo,'amount':add,'date':realdate}
								remm.append(gh)
						if k =='fff':
							datasdict={'remm':remm,'udate':realdate}
							all_data.append(datasdict)
				
				return render_to_response('thrift/monthrep.html',{'company':mybranch, 'user':varuser,
					'thriftrec':all_data,'status':status,'month':realmonth,'year':yday})
		
	
		else:
			form=viewallapprovedform()
		return render_to_response('thrift/approvalsreport.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/')


def payout(request):
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

		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			form = viewmerchantform(request.POST)
			if form.is_valid():
				merchant=form.cleaned_data['merchant']
				datte=form.cleaned_data['date'] #JS date Object
				yday,mday,dday = datte.split('/')

				try:
					memmerchant=tblMERCHANT.objects.get(id=merchant,status=1,branch=mybranch)
				except:
					return render_to_response('404.html',{'company':mybranch, 'user':varuser})

				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				month=calendar.month_name[mday]

				mydate=date(yday,mday,dday)

				ddt=[]
				
				frf=[]

				allunpaid= tblpayoutrequest.objects.filter(merchant=memmerchant,branch=mybranch,date=mydate,
					month=month,status='Unpaid')

				mycost=[]
				myc=[int(q.customer.id) for q in allunpaid]
				[mycost.append(x) for x in myc if x not in mycost] #removes duplicates in lost

				for kid in mycost:
					customer=tblCUSTOMER.objects.get(id = kid,status=1)
					rtpp = tblpayoutrequest.objects.filter(customer=customer,date=mydate,
						month=month,status='Unpaid')

					custo=rtpp.aggregate(Sum('amount'))
					custo = custo['amount__sum']
					fd ={'sum':custo,'customer':customer}
					frf.append(fd)

				add = allunpaid.aggregate(Sum('amount'))
				add = add['amount__sum']
				dl={'total':add}
				ddt.append(dl)

				return render_to_response('thrift/adminpayout.html',{'total':ddt,'company':mybranch,'merchant':merchant,
							'user':varuser,'mydate':mydate,'date':datte,'thriftrec':frf})
			else:
				return render_to_response('thrift/adminnopay.html',{'company':mybranch,'user':varuser})
				
		else:
			form=viewmerchantform()
		return render_to_response('thrift/payout.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')



def canceloptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate=acccode.split(':')

    		return render_to_response('thrift/admiinpayoutoption.html',{'date1':trandate,'customer':state})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')



def withdrawoptions(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		state,trandate=acccode.split(':')

    		return render_to_response('thrift/adminwithdrawfund.html',{'date1':trandate,'customer':state})
    	else:
    		return HttpResponseRedirect('/login/')
    else:
    	return HttpResponseRedirect('/login/')


def cancelreq(request,vid):
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

		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			customer=request.POST['customer']
			datte=request.POST['date1'] #JS date Object
			yday,mday,dday = datte.split('/')

			yday=int(yday)
			mday=int(mday)
			dday=int(dday)

			mydate=date(yday,mday,dday) #python date object
			month=calendar.month_name[mday]

			customer=tblCUSTOMER.objects.get(id=vid)

			allreq = tblpayoutrequest.objects.filter(status='Unpaid',branch=mybranch,month=month,
				date=mydate,customer = customer)

			transactions = tblthrift_trans.objects.filter(branch=mybranch,reason='Requsted',
				avalability='Available',recdate__month=mday,customer=customer)
			
			code=[]

			for j in allreq:
				dc=j.code
			 	for k in transactions:
			 		trans_code = int(k.code)
			 		code.append(trans_code)
			 		if dc==trans_code:
			 			k.reason='Available'
			 			k.save()
			 			j.delete()
			return render_to_response('thrift/reqestcancel.html',{'company':mybranch,'user':varuser})

	else:
		return HttpResponseRedirect('/login/')


def withdrawfunds(request,vid):
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

		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':
			customer=request.POST['customer']
			datte=request.POST['date1'] #JS date Object
			yday,mday,dday = datte.split('/')

			yday=int(yday)
			mday=int(mday)
			dday=int(dday)

			mydate=date(yday,mday,dday) #python date object
			month=calendar.month_name[mday]

			customer=tblCUSTOMER.objects.get(id=vid)
			merchant=customer.merchant.id
			merchant=tblMERCHANT.objects.get(id=merchant)


			allreq = tblpayoutrequest.objects.filter(status='Unpaid',branch=mybranch,month=month,
				date=mydate,customer = customer)
			mycount=allreq.count()


			add=allreq.aggregate(Sum('amount'))
			payable_sum = add['amount__sum']

			# if l == 0:
			# 	k = random.randint(0,9)
			# 	y = random.randint(0,9)
			# 	x = random.randint(0,9)
			# 	z = random.randint(0,9)
			# 	a = random.randint(0,9)
			# 	pin =  str(k) + str(y) + str(x) + str(z)+ str(a)


			transactions = tblthrift_trans.objects.filter(branch=mybranch,reason='Requsted',avalability='Available',
				recdate__month=mday,customer=customer)

			
		
			for j in allreq:
				dc=j.code #field is integer
				amount=j.amount
			 	for k in transactions:
			 		trans_code = int(k.code) #field is charfield
			 		if dc==trans_code:			 			
			 			k.delete()
			 			j.delete()

			if mycount> 0:

				# daterr=date.today()
				fdate= datetime.today()
				daterr=date(fdate.year,fdate.month,fdate.day)

				tblpayoutrecord(month =month ,status='Paid',branch=mybranch,customer=customer,
					amount=payable_sum,paid_by=varuser,merchant=merchant,recdate=daterr).save()

				customer=customer.surname +" " + customer.firstname + " " + customer.othername
				return render_to_response('thrift/reqestwithdrawsuccess.html',{'company':mybranch,'user':varuser,'amount':payable_sum,'customer':customer})

	else:
		return HttpResponseRedirect('/login/')


def adminpayfund(request):
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

		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method == 'POST':

			merchant= request.POST['merchant']
			datte=request.POST['date'] #date the request was made
			
			merchant=tblMERCHANT.objects.get(id=merchant,status=1)

			yday,mday,dday = datte.split('/')

			yday=int(yday)
			mday=int(mday)
			dday=int(dday)

			mydate=date(yday,mday,dday)

			month=calendar.month_name[mday]

			ddt=[]

			allunpaid= tblpayoutrequest.objects.filter(merchant=merchant,branch=mybranch,date=mydate,
				month=month,status='Unpaid') #request by all customers thru the merchant

			mycost=[]
			myc=[int(q.customer.id) for q in allunpaid]
			[mycost.append(x) for x in myc if x not in mycost] #Unique list of customers who request cash

			mycount= len(mycost)
			

			transactions = tblthrift_trans.objects.filter(merchant=memmerchant,branch=mybranch,
				reason='Requsted',avalability='Available',recdate__month=mday)
			
			code=[]
			for k in allunpaid: #Allunpaid = gross number of requests
				customer=k.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)

				try:
					tblpayoutrecord.objects.get(branch=mybranch,merchant=merchant,customer=customer,recdate=mydate,
						amount=k.amount,status='Paid')
				except:
					tblpayoutrecord(branch=mybranch,merchant=merchant,customer=customer,amount=k.amount,status='Paid',
						recdate=mydate).save()
					code.append(int(k.code))

					k.delete()
			

			for j in transactions:
				dc=j.code
				customer=j.customer.id
				customer=tblCUSTOMER.objects.get(id=customer,status=1)

			 	for k in code:
			 		trans_code = int(k.code)
			 		code.append(trans_code)
			 		if dc==k:
			 			k.reason='Withdrawn'
			 			k.save()
			 			j.delete()

			return render_to_response('thrift/adminpayoutsuccess.html',{'count':mycount,'company':mybranch,'merchant':merchant,'user':varuser})

		else:
			form=viewmerchantform()
		return render_to_response('thrift/payout.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')



def payoutreport(request):
	if 'userid' in request.session:
		varuser=request.session['userid']

		staff = Userprofile.objects.get(email=varuser,status=1)
		if staff.thrift==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
			# return render_to_response('404.html')

		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)

## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		memstaff = tblSTAFF.objects.get(branch=mybranch,id=staffdet)
		if request.method == 'POST':
			form = payoutform(request.POST)
			if form.is_valid():
				status=form.cleaned_data['status']
				date1=form.cleaned_data['date']
				yday,mday,dday = date1.split('/')

				yday=int(yday)
				mday=int(mday)
				dday=int(dday)
				mydate=date(yday,mday,dday)
				month = calendar.month_name[mday]
								
				allmerchant = tblMERCHANT.objects.filter(branch=mybranch,status=1)
				remm=[]
				all_data=[]

				if 'checkbox' in request.POST:
					checkbox=request.POST['checkbox']
				else:
					checkbox=1
				
				if checkbox==1:
					if status == 'Paid':						
						for k in allmerchant:
							thriftrec= tblpayoutrecord.objects.filter(branch=mybranch,recdate=mydate,merchant=k)
							add=0
							add = thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']
							if add > 0:
								gh={'my_merchant':k,'amount':add}
								remm.append(gh)

					elif status == 'Pending':
						for p in allmerchant:
							thriftrec= tblpayoutrequest.objects.filter(month=month,status='Unpaid', branch=mybranch,date=mydate,merchant=p)
							add =0
							
							add=thriftrec.aggregate(Sum('amount'))
							add = add['amount__sum']

							if add > 0:
								gh={'my_merchant':p,'amount':add}
								remm.append(gh)
						
					return render_to_response('thrift/payoutdayreport.html',{'company':mybranch,'user':varuser,
						'thriftrec':remm,'date':mydate,'fund':status})

				else: # if checkbox == month


					P = (monthrange(yday, mday))[-1]
					for n in range (P,0,-1):		
						realdate = date(yday,mday,n)
						k =0
						if status=='Remitted':
							for mn in allmerchant:								
								thriftrec= tblmerchantBank.objects.filter(branch=mybranch,recdate=realdate,merchant=mn)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':mn,'amount':add,'month':realdate}
									remm.append(gh)

							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)

						elif status == 'Unremmitted':
							for kl in allmerchant:
								thriftrec= tblMerchantTrans.objects.filter(remitted='Unremmitted',approved='Not Approved', branch=mybranch,recdate=realdate,merchant=kl)
								if thriftrec.count() > 0:
									k = 'fff'
									add=thriftrec.aggregate(Sum('amount'))
									add = add['amount__sum']
									gh={'my_merchant':kl,'amount':add,'month':realdate}
									remm.append(gh)
							if k =='fff':
								datasdict={'remm':remm,'udate':realdate}
								all_data.append(datasdict)


		else:
			form=payoutform()
		return render_to_response('thrift/payoutreport.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')

#######******** ceo reports *********************
def repome(request):
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
		return render_to_response('thrift/reporthome.html',{'company':mybranch, 'user':varuser})
	else:
		return HttpResponseRedirect('/login/')

def merchantreport(request):
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
		form=merchantreportform()
		return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/')

def getmerchantid(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk = []
    		sdic = {}
    		data = Userprofile.objects.get(email = acccode, ceo=1)
    		branchcode = data.branch.id
    		branchcode=tblBRANCH.objects.get(id=branchcode)

    		allmerchants = tblMERCHANT.objects.filter(branch=branchcode, status=1)
    		
    		for j in allmerchants:
    			j = j.id
    			s = {j:j}
    			sdic.update(s)
    		klist = sdic.values()
    		for p in klist:
    			kk.append(p)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')

		# else:
		# 	gdata = ""
		# 	return render_to_response('index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')



def getmerchantname(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk=[]
    		data=tblMERCHANT.objects.get(id=acccode,status=1)
    		data =data.staff.id
    		data = tblSTAFF.objects.get(id =data)
    		j = data.surname #+ " " + data.firstname+ " " + data.othername
    		kk.append(j)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')
    	else:
    		gdata = ""
    		return render_to_response('index.html',{'gdata':gdata})
    else:
    	return HttpResponseRedirect('/login/')




def getmereportajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,name,dates,report= acccode.split(':')
                stlist = []

                # if dates == "":
                # 	dates =date.today()

                dday,mday,yday = dates.split('/') #JSON Dates Object
                yday=int(yday)
                mday=int(mday)
                dday=int(dday)
                oydate=date(yday,mday,dday)
                weekday=int(date(yday,mday,dday).isocalendar()[1])
                relmerchant = tblMERCHANT.objects.get(id=ID,status=1)

                if report == 'daily':
                	merc = tblmerchantBank.objects.filter(merchant=relmerchant,recdate=oydate)
                elif report == 'weekly':
                	merc= tblmerchantBank.objects.filter(merchant=relmerchant,weekno=weekday)
              
                elif report== 'monthly':
                	merc=tblmerchantBank.objects.filter(merchant=relmerchant,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('thrift/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/')





def cashierreport(request):
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

		form=cashreportform()
		return render_to_response('thrift/reportcash.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/')


def getcashid(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk = []
    		sdic = {}
    		data = Userprofile.objects.get(email = acccode, ceo=1)

    		branchcode = data.branch.id
    		branchcode=tblBRANCH.objects.get(id=branchcode)

    		allcashier = Userprofile.objects.filter(cashier=1,status=1,branch=branchcode)
    		
    		for j in allcashier:
    			j = j.staffrec.id  #uses ID from tblSTAFF
    			s = {j:j}
    			sdic.update(s)
    		klist = sdic.values()
    		for p in klist:
    			kk.append(p)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')

		# else:
		# 	gdata = ""
		# 	return render_to_response('index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')

def getcashname(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk=[]

    		data=tblSTAFF.objects.get(id=acccode)
    		j = data.surname
    		kk.append(j)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')
    	else:
    		gdata = ""
    		return render_to_response('index.html',{'gdata':gdata})
    else:
    	return HttpResponseRedirect('/login/')


def getcashreportajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,name,dates,report= acccode.split(':')
                stlist = []

                # if dates == "":
                # 	dates =date.today()
                # else:
                # 	dates = request.POST['date']

                dday,mday,yday = dates.split('/') #JSON Dates Object
                yday=int(yday)
                mday=int(mday)
                dday=int(dday)
                oydate=date(yday,mday,dday)
                weekday=int(date(yday,mday,dday).isocalendar()[1])

                relcashier = tblSTAFF.objects.get(id=ID)
                relcashier=relcashier.email
              
                if report == 'daily':
                	merc = tblmerchantBank.objects.filter(remitted_by =relcashier,recdate=oydate)
                elif report == 'weekly':
                	merc= tblmerchantBank.objects.filter(remitted_by=relcashier,weekno=weekday)
              
                elif report== 'monthly':
                	merc=tblmerchantBank.objects.filter(remitted_by=relcashier,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('thrift/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/')



def adminreport(request):
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

		form=adminreportform()
		return render_to_response('thrift/reportadmin.html',{'company':mybranch, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/')




def getadminid(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk = []
    		sdic = {}
    		data = Userprofile.objects.get(email = acccode, ceo=1)

    		branchcode = data.branch.id
    		branchcode=tblBRANCH.objects.get(id=branchcode)

    		alladmin = Userprofile.objects.filter(admin=1,status=1,branch=branchcode)
    		
    		for j in alladmin:
    			j = j.staffrec.id
    			s = {j:j}
    			sdic.update(s)
    		klist = sdic.values()
    		for p in klist:
    			kk.append(p)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')

		# else:
		# 	gdata = ""
		# 	return render_to_response('index.html',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')

def getadminname(request):
    if request.is_ajax():
    	if request.method == 'POST':
    		post = request.POST.copy()
    		acccode = post['userid']
    		kk=[]
    		data=tblSTAFF.objects.get(id=acccode)
    		j = data.surname
    		kk.append(j)
    		return HttpResponse(json.dumps(kk), mimetype='application/json')
    	else:
    		gdata = ""
    		return render_to_response('index.html',{'gdata':gdata})
    else:
    	return HttpResponseRedirect('/login/')

def getadminreportajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,name,dates,report= acccode.split(':')
                stlist = []

                # if dates == "":
                # 	dates =date.today()
                # else:
                # 	dates = request.POST['date']

                dday,mday,yday = dates.split('/') #JSON Dates Object
                yday=int(yday)
                mday=int(mday)
                dday=int(dday)
                oydate=date(yday,mday,dday)
                weekday=int(date(yday,mday,dday).isocalendar()[1])

                relcashier = tblSTAFF.objects.get(id=ID)
                relcashier=relcashier.email
              
                if report == 'daily':
                	merc = tblmerchantBank.objects.filter(remitted_by =relcashier,recdate=oydate)
                elif report == 'weekly':
                	merc= tblmerchantBank.objects.filter(remitted_by=relcashier,weekno=weekday)
              
                elif report== 'monthly':
                	merc=tblmerchantBank.objects.filter(remitted_by=relcashier,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('thrift/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/')

def getadminreportajax(request):
    if  "userid" in request.session:
        if request.is_ajax():
            if request.method == 'POST':
                varuser = request.session['userid']
                varerr =""
                post = request.POST.copy()
                acccode = post['userid']
                ID,name,dates,report= acccode.split(':')
                stlist = []

                # if dates == "":
                # 	dates =date.today()
                # else:
                # 	dates = request.POST['date']

                dday,mday,yday = dates.split('/') #JSON Dates Object
                yday=int(yday)
                mday=int(mday)
                dday=int(dday)
                oydate=date(yday,mday,dday)
                weekday=int(date(yday,mday,dday).isocalendar()[1])

                relcashier = tblSTAFF.objects.get(id=ID)
                relcashier=relcashier.email
              
                if report == 'daily':
                	merc = tblmerchantBank.objects.filter(approved_by =relcashier,recdate=oydate)
                elif report == 'weekly':
                	merc= tblmerchantBank.objects.filter(approved_by=relcashier,weekno=weekday)
              
                elif report== 'monthly':
                	merc=tblmerchantBank.objects.filter(approved_by=relcashier,recdate__month=mday)

                if merc.count() == 0:
                	add = 0
                else:
                	addw = merc.aggregate(Sum('amount'))
                	add = addw['amount__sum']
                return render_to_response('thrift/dailyreport.html',{'name':name,'total':add,'report':report})

            else:
            	return HttpResponseRedirect('/thrift/thrift/reports/sales/merchant/')
        else:
        	return render_to_response('thrift/reportmerchant.html',{'company':mybranch, 'user':varuser,'form':form})
    else:
   		return HttpResponseRedirect('/login/')

