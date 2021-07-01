from django.shortcuts import render_to_response
from django.http import  Http404, HttpResponseRedirect, HttpResponse

from sysadmin.models import *
# from partner.models import *






def index(request):
	if request.method=='POST':
		email=request.POST['email']
		password=request.POST['password']
		try:			
			user=Userprofile.objects.get(email=email,password=password)
			request.session['userid'] = user.email
			varuser = request.session['userid']
			return  HttpResponseRedirect('/dashboard/')
		except:
			return HttpResponseRedirect('/login/')

	else:
		return render_to_response('index.html')
		# return render_to_response('login.html')

def login(request):
	if request.method=='POST':
		email=request.POST['email']
		password=request.POST['password']
		try:			
			user=Userprofile.objects.get(email=email,password=password)
			request.session['userid'] = user.email
			varuser = request.session['userid']
			return  HttpResponseRedirect('/dashboard/')
		except:
			return HttpResponseRedirect('login.html')

	else:
		# return render_to_response('index.html')
		return render_to_response('login.html')


def dashboard(request):
	if 'userid' in request.session:
		varuser = request.session['userid']
		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			return HttpResponseRedirect('/login/')

		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)
		staff = Userprofile.objects.filter(email=varuser,status=1)
		return render_to_response('dashboard.html',{'user':varuser,'company':mybranch,
			'menu':staff})
	else:
		return HttpResponseRedirect('/login/')


def logoutuser(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/')

def switchuser(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/user/')

def changepass(request):
	if 'userid' in request.session:
		varuser = request.session['userid']

		try:
			staff = Userprofile.objects.get(email=varuser,status=1)
		except:
			return HttpResponseRedirect('/login/')
		
		staffdet=staff.staffrec.id
		branch=staff.branch.id
		mycompany=staff.branch.company
		company=mycompany.name
		comp_code=mycompany.id
		ourcompay=tblCOMPANY.objects.get(id=comp_code)
		mybranch=tblBRANCH.objects.get(company=ourcompay,id=branch)

		if request.method=='POST': 
			oldpass= request.POST['oldpass']
			newpass1=request.POST['newpass1']
			newpass2=request.POST['newpass2']

			if oldpass== staff.password : 
				if newpass2 == newpass1: 
					msg= 'password change successfull'
					rr=Userprofile.objects.filter(email=varuser,status=1).update(password=newpass1)
					return render_to_response('success.html',{'user':varuser,'company':mybranch,
						'menu':staff,'msg':msg})
				else:
					msg = 'the passwords do not match'
			else: 
				msg='your old pass is not correct'


		else : 
			msg=''


		
		return render_to_response('changepass.html',{'user':varuser,'company':mybranch,
				'menu':staff,'msg':msg})

	else:
		return HttpResponseRedirect('/login/')



def tutorial(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect('/login/')