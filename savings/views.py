from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from savings.forms import *
from sysadmin.models import *
from savings.models import *


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
		

		return render_to_response('savings/welcome.html',{'company':mybranch, 'user':varuser})
	
	else:
		return HttpResponseRedirect('/login/')





def openaccount(request):
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

		if staff.account_officer == 1 : 
			pass
		else: 
			return render_to_response('savings/404.html',{'company':mybranch, 'user':varuser})

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
					countt=tblCUSTOMER.objects.get(wallet=wallet)
				
				except:
		#### staff makes self a merchant
					tblMERCHANT(branch=mybranch,staff=memstaff,status=0,code=673).save()
					memmerchant=tblMERCHANT.objects.get(staff=memstaff,branch=mybranch)



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
		return render_to_response('savings/openaccount.html',{'company':mybranch, 'user':varuser,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def withdraw(request):
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

		# try:
		# 	memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		# except:
		# 	return render_to_response('404.html',{'company':mybranch, 'user':varuser})
					
		# mydate=date.today().month
		# month= calendar.month_name[mydate]
		# datee= date.today()

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(wallet=mywallet,status=1,
						merchant=memmerchant,branch=mybranch)
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
					
				return render_to_response('thrift/paythrift.html',{'company':mybranch,'date':datee, 'month':month,'thrift':mythrift,'user':varuser,'form':myform,
						'wallet':mywallet,'thriftrec':thriftrec})
				
			else:
				pass

		else:
			form=viewwalletform()
		return render_to_response('savings/withdraw.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')



def deposit(request):
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

		# try:
		# 	memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		# except:
		# 	return render_to_response('404.html',{'company':mybranch, 'user':varuser})
					
		# mydate=date.today().month
		# month= calendar.month_name[mydate]
		# datee= date.today()

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(wallet=mywallet,status=1,
						merchant=memmerchant,branch=mybranch)
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
					
				return render_to_response('thrift/paythrift.html',{'company':mybranch,'date':datee, 'month':month,'thrift':mythrift,'user':varuser,'form':myform,
						'wallet':mywallet,'thriftrec':thriftrec})
				
			else:
				pass

		else:
			form=viewwalletform()
		return render_to_response('savings/deposit.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')


def balances(request):
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

		# try:
		# 	memmerchant=tblMERCHANT.objects.get(staff=memstaff,status=1)
		# except:
		# 	return render_to_response('404.html',{'company':mybranch, 'user':varuser})
					
		# mydate=date.today().month
		# month= calendar.month_name[mydate]
		# datee= date.today()

		if request.method == 'POST':
			form = viewwalletform(request.POST)
			if form.is_valid():
				mywallet=form.cleaned_data['wallet']
				try:
					details=tblCUSTOMER.objects.get(wallet=mywallet,status=1,
						merchant=memmerchant,branch=mybranch)
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
					
				return render_to_response('thrift/paythrift.html',{'company':mybranch,'date':datee, 'month':month,'thrift':mythrift,'user':varuser,'form':myform,
						'wallet':mywallet,'thriftrec':thriftrec})
				
			else:
				pass

		else:
			form=viewwalletform()
		return render_to_response('savings/balance.html',{'company':mybranch, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')