from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from staff.forms import *
from sysadmin.models import *
from staff.models import *
from datetime import date
import calendar

from django.db.models import Max,Sum
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
		
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('staff/welcome.html',{'company':mybranch, 'user':varuser})
		
	else:
		return HttpResponseRedirect('/login/')


def newst(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff = Userprofile.objects.get(email=varuser,status=1)

		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})		
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
	
		if request.method == 'POST':
			surname=request.POST['surname']
			firstname= request.POST['firstname']
			othername=request.POST['othername']
			phone=request.POST['phone']
			address=request.POST['address']
			email = request.POST['email']

			phone=phone.split(' ')
			phone = str(phone[0]+phone[1]+phone[2])
			try:
				phone=int(phone)
			except:
				return render_to_response('staff/staffdet.html',{'company':mybranch, 'user':varuser})

			wallet=phone
			
			try:
				countt=tblSTAFF.objects.get(email=email) #whether active or not
				msg = "EMAIL ALREADY EXIST"
				return render_to_response('staff/staffdet.html',{'company':mybranch, 
					'user':varuser,'msg':msg})
			except: 

				tblSTAFF(surname=surname,firstname=firstname,othername=othername, status=1,phone=phone,Address=address,code=68768,email=email,branch=mybranch,types='Field').save()

				myuser =tblSTAFF.objects.get(email=email)  #whether active or not 

				Userprofile(status=1,branch=mybranch,code=20698,ceo=0,

					thrift=0, cashier=0,admin=0,thrift_officer=0,
					loan_thrift=0, loan_thrift_admin=0, loan_thift_officer= 0,

					savings=0, save_admin=0,   account_officer =0,
					loan=0,    loan_admin=0,   loan_officer=0,
					
					coop=0,    coop_admin=0,   coop_officer =0,

					staffrec=myuser,partner=0,password='thrift',email=email).save()

			return render_to_response('staff/success.html',{'company':mybranch,'user':varuser,'email':email})

		else:
			return render_to_response('staff/staffdet.html',{'company':mybranch, 'user':varuser})
		
	else:
		return HttpResponseRedirect('/login/')



def regmerchant(request):
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
		
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		if request.method== 'POST':
			form = staffform(request.POST)

			if form.is_valid():
				email=form.cleaned_data['email']


				mystaff = tblSTAFF.objects.filter(email=email,status=1) #check status
				mycount=mystaff.count()


				appps = tblapp.objects.get(branch=branch)

				if mycount == 1:
					querry_email = tblSTAFF.objects.get(email=email)
					
					try:
						tblMERCHANT.objects.get(staff=querry_email)
						msg='ALREADY REGISTERED'
					
					except:
						if appps.thrift== 1 : 
							
							diff = Userprofile.objects.get(email=email,status=1)
							diff.thrift_officer=1
							diff.thrift=1
							diff.save()
							form = staffform()
							msg="SUCCESSFUL"

							mym= tblSTAFF.objects.get(email=email)
							tblMERCHANT(branch=mybranch,staff=mym,status=1,code=673).save()
					
				else:
					msg = 'THIS EMAIL IS NOT REGISTERED'
			else:
				msg = 'INVALID ENTRY'
		else:
			form = staffform()
			msg=''

		return render_to_response('staff/merch.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})
	else:
		return HttpResponseRedirect('/login/')



def tutorial(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})		
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id

		ourcompay=tblCOMPANY.objects.get(id=comp_code)


## use this in thee future
		# comp_code=mycompany.code
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		return render_to_response('staff/adminwelcome.html',{'company':mybranch, 'user':varuser})
		# pass
	else:
		return HttpResponseRedirect('/login/')


def roles(request):
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
		
		if staff.ceo==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		
		stafflist = Userprofile.objects.filter(branch=mybranch,status=1).exclude(email='njc@gmail.com')
		mystafflist=[]
		for  k in stafflist:
			name=k.staffrec.surname + "  " + k.staffrec.firstname +"  "+ k.staffrec.othername
			ID = k.staffrec.id
			s= {'name':name,'id':ID}
			mystafflist.append(s)
			
		return render_to_response('staff/stafflist.html',{'company':mybranch, 'user':varuser,'list':mystafflist})

	else:
		return HttpResponseRedirect('/login/')


def setroles(request):
	if  "userid" in request.session:
		if request.is_ajax():
			if request.method == 'POST':
				varuser = request.session['userid']
				varerr =""
				post = request.POST.copy()
				acccode = post['userid']

				stafflist = tblSTAFF.objects.get(id = acccode)
				userlist = Userprofile.objects.get(staffrec=stafflist,status=1)
				
				myy=[]
				name = stafflist.surname + " " + stafflist.firstname + " " + stafflist.othername
				

#######thrifts********************
				if userlist.cashier is True:
					cashier= 'checked'
				else:
					cashier='unchecked'
				if userlist.admin is True:
					admin='checked'
				else:
					admin='unchecked'


#############loan*******************
				if userlist.loan_officer is True:
					loan_officer= 'checked'
				else:
					loan_officer='unchecked'

				if userlist.loan_admin is True:
					loan_admin='checked'
				else:
					loan_admin='unchecked'


#####savings*************************
				if userlist.save_admin is True:
					save_admin= 'checked'
				else:
					save_admin='unchecked'

				if userlist.account_officer is True:
					account_officer='checked'
				else:
					account_officer='unchecked'


####coop*****************
				if userlist.coop_admin is True:
					koopad= 'checked'
				else:
					koopad ='unchecked'
				if userlist.coop_officer is True:
					kopo='checked'
				else:
					kopo='unchecked'


				s= {'name':name ,
				'cash':cashier,'adm':admin,
				'loana':loan_admin , 'loano':loan_officer,
				'savea':save_admin,'saveo':account_officer,
				'coopa':koopad,'coopo':kopo}

				myy.append(s)
				return render_to_response('staff/staffroles.html',{'list':myy,'ID':acccode})
			else:
				gdata = ""
				return render_to_response('index.html',{'gdata':gdata})
		else:
			gdata = ""
			return render_to_response('getlg.htm',{'gdata':gdata})
	else:
		return HttpResponseRedirect('/login/')

def updaterole(request,vid):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})

		thestaff = tblSTAFF.objects.get(id=vid)

 #Thrifts*********************
		if 'mycashier' in request.POST:
			cashier=request.POST['mycashier']
			Userprofile.objects.filter(staffrec= thestaff).update(cashier=cashier)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(cashier=0)
		

		if 'myadmin' in request.POST:
			admin=request.POST['myadmin']
			Userprofile.objects.filter(staffrec= thestaff).update(admin=1)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(admin=0)
		
		
#savings************************

		if 'myao' in request.POST:
			ao=request.POST['myao']
			Userprofile.objects.filter(staffrec= thestaff).update(account_officer=1)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(account_officer=0)

		if 'saveadmin' in request.POST:
			sa=request.POST['saveadmin']
			Userprofile.objects.filter(staffrec= thestaff).update(save_admin=1)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(save_admin=0)


###loans**************************
		if 'loancashier' in request.POST:
			lc=request.POST['loancashier']
			Userprofile.objects.filter(staffrec= thestaff).update(loan_officer=lc)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(loan_officer=0)
		
		if 'loanadmin' in request.POST:
			la=request.POST['loanadmin']
			Userprofile.objects.filter(staffrec= thestaff).update(loan_admin=la)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(loan_admin=0)

###coorp**************************

		if 'coopoffis' in request.POST: 
			co=request.POST['coopoffis']
			Userprofile.objects.filter(staffrec= thestaff).update(coop_officer=co)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(coop_officer=0)

		if 'coopaadmin' in request.POST: 
			ca=request.POST['coopaadmin']
			Userprofile.objects.filter(staffrec= thestaff).update(coop_admin=ca)
		else:
			Userprofile.objects.filter(staffrec= thestaff).update(coop_admin=0)
		return HttpResponseRedirect('/staff/staff/roleplay/')

	else:
		return HttpResponseRedirect('/login/')

def viewdetail(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		if staff.admin==0:
			return render_to_response('404.html',{'company':mybranch, 'user':varuser})
		staffdet=staff.staffrec.id

		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)

		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		if request.method=='POST':
			form = staffform(request.POST)

			if form.is_valid():
				email=form.cleaned_data['email']

				mystaff = tblSTAFF.objects.filter(email=email,status=1) #check status
				mycount=mystaff.count()

				if mycount == 1:
					msg= ''
					querry_email = tblSTAFF.objects.get(email=email)
					return render_to_response('staff/myprofile.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})
					
				else:
					msg = 'THIS EMAIL IS NOT REGISTERED'
			else:
				msg = 'INVALID ENTRY'
		else:
			form = staffform()
			msg=''

		return render_to_response('staff/profdetail.html',{'company':mybranch,'msg':msg, 'user':varuser,'form':form})
		
	else:
		return HttpResponseRedirect('/login/')