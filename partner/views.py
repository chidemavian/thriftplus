from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse
from partner.forms import *
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
		
		if staff.partner==0:
			return render_to_response('404.html')

		return render_to_response('partner/welcome.html',{'company':mybranch, 'user':varuser})
		
	else:
		return HttpResponseRedirect('/login/')


def registration(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)

		if staff.partner==0:
			return render_to_response('404.html')
		if request.method == 'POST':
			name=request.POST['Name']
			web=request.POST['website']
			insta = request.POST['instagram']
			facebook = request.POST['facebook']
			twit= request.POST['twitter']
			youtube = request.POST['youtube']
			try:
				mycom = tblCOMPANY.objects.get(name=name)
			except:
				tblCOMPANY(engine='tts',web=web,code='43',name=name,twitter=twit,
					youtube=youtube,fb=facebook,ux=0,logo='company_logo/thrift.png',
					partner=partnerfff,ig=insta,size=20).save()
				mycom = tblCOMPANY.objects.get(name=name)
				
				return render_to_response('partner/busregistersuccess.html',{'company':mybranch,'user':varuser,'business':mycom})
		else:
			pass

		return render_to_response('partner/register.html',{'company':mybranch,'user':varuser})

	else:
		return HttpResponseRedirect('/login/')


def branch(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)


		if staff.partner==0:
			return render_to_response('404.html')

		
		if request.method == 'POST':
			form = companyform(request.POST)

			if form.is_valid():
				companygg= form.cleaned_data['company']

			try:
				k = tblCOMPANY.objects.get(id =companygg,partner=partnerfff)
				return render_to_response('partner/savebus.html',{'company':mybranch,'user':varuser,'comp':k})
			except:
				return render_to_response('partner/branch.html',{'company':mybranch,'user':varuser,'form':form}) 
		else:
			form = companyform()

		return render_to_response('partner/branch.html',{'company':mybranch,'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/')


def branch1(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)
		if staff.partner==0:
			return render_to_response('404.html')
		if request.method=='POST':
			partnerfff = tblPARTNER.objects.get(email=varuser)
			company=request.POST['company']
			k = tblCOMPANY.objects.get(id =company,partner=partnerfff)
			return render_to_response('partner/savebus.html',{'company':mybranch,'user':varuser,'comp':k})

	else:
		return HttpResponseRedirect('/login/')




def address(request):
	if 'userid' in request.session:
		varuser=request.session['userid']
		staff=Userprofile.objects.get(email=varuser, status=1)
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if staff.partner==0:
			return render_to_response('404.html')

		if request.method == 'POST':
			address= request.POST['address']
			phone = request.POST['phone']
			company=request.POST['company']

			phone=phone.split(' ')
			phone = str(phone[0]+phone[1]+phone[2])

			try:
				phone=int(phone)
			except:
				msg = 'Incomplete phone number'
				return render_to_response('partner/branch.html',{'company':mybranch,'user':varuser})

			det=[]
			partner=tblPARTNER.objects.get(email=varuser)

			try:
				k = tblCOMPANY.objects.get(id =company,partner=partner)
				tblBRANCH(company=k,code=k.code,Address=address,phone=phone,types='Head').save()
				bre = tblBRANCH.objects.get(company=k)
				return render_to_response('partner/branchsuccess.html',{'company':mybranch,'user':varuser,'comp':bre})
			except:
				return render_to_response('partner/branch.html',{'company':mybranch,'user':varuser}) 
		else:
			form = companyform()

		return render_to_response('partner/branch.html',{'company':mybranch,'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/')



def ceo(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)
		if staff.partner==0:
			return render_to_response('404.html')

		if request.method == 'POST':
			form = companyform(request.POST)
			detail =[]

			if form.is_valid():
				companygg= form.cleaned_data['company']
			try:
				k = tblCOMPANY.objects.get(id =companygg,partner=partnerfff)
				ad= tblBRANCH.objects.get(company=k)
				jk = {'name':k.name.upper(),'address':ad.Address,'id':k.id}
				detail.append(jk)
				return render_to_response('partner/ceoreg.html',{'company':mybranch,'user':varuser,'comp':detail})
			except:
				return render_to_response('partner/ceo.html',{'company':mybranch,'user':varuser,'form':form}) 
		else:
			form = companyform()

		return render_to_response('partner/ceo.html',{'company':mybranch,'user':varuser,'form':form})

	else:
		return HttpResponseRedirect('/login/')



def ceo1(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)
		if staff.partner==0:
			return render_to_response('404.html')


		detail=[]

		if request.method == 'POST':
			company= request.POST['company']
			k = tblCOMPANY.objects.get(id =company,partner=partnerfff)
			ad= tblBRANCH.objects.get(company=k)
			jk = {'name':k.name.upper(),'address':ad.Address,'id':k.id}
			detail.append(jk)
			return render_to_response('partner/ceoreg.html',{'company':mybranch,'user':varuser,'comp':detail})
	else:
		return HttpResponseRedirect('/login/')


def regceo(request):
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
		partnerfff=tblPARTNER.objects.get(email=varuser)
		if staff.partner==0:
			return render_to_response('404.html')

		if request.method == 'POST':
			company=request.POST['company']
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
				msg = 'Incomplete phone number'
				return render_to_response('thrift/createwallet.html',{'company':mybranch, 'user':varuser,'msg':msg})

			try:
				staff= tblstaff.objects.get(email=email)
				return render_to_response('partner/ceoreg.html',{'company':mybranch,'user':varuser,'comp':detail})
			except:
				k = tblCOMPANY.objects.get(id =company,partner=partnerfff)
				branch= tblBRANCH.objects.get(company=k)
				
				tblSTAFF(branch=branch,status = 1, code=k.code,surname=surname,firstname=firstname,
					othername=othername,photo='staff-pix/user.png',email=email,
					phone=phone,Address=address,types='Field').save()

				staff= tblSTAFF.objects.get(email=email)


				tblMERCHANT(branch=branch,staff=staff,status=1,code=673).save()


###in the future, i'll seperate the next two lines************

				tblapp(branch=branch,thrift=1,partner=partnerfff).save()		
				Userprofile(status=1,branch=branch,code=k.code,ceo=1,

					thrift=1, cashier=1,admin=1,thrift_officer=1,
					loan_thrift=0, loan_thrift_admin=1, loan_thift_officer=1,

					savings=0, save_admin=1,   account_officer =1,
					loan=0,    loan_admin=1,   loan_officer=1,
					
					coop=0,    coop_admin=1,   coop_officer =1,
					staffrec=staff,partner=0,password=12345,email=email).save()

				return render_to_response('partner/ceosuccess.html',{'company':mybranch,'user':varuser}) 
	else:
		return HttpResponseRedirect('/login/')