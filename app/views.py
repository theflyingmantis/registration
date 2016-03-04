from django.shortcuts import render,render_to_response,redirect
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from app.models import *
from django.contrib import messages

def index(request):
	c = {}
	error=None
	c.update(csrf(request))
	request.session['s_logged'] = False
	request.session['money_paid'] = False
	if request.method=="POST":
		id1= request.POST.get('id', '')
		password = request.POST.get('password', '')
		type1=request.POST.get('type', '')
		
		if type1=='student':
			try:
				q=student.objects.get(id1=id1)
				if q.password==password:
					request.session['s_logged'] = True
					request.session['s_id'] = q.id
					messages.success(request, 'User authenticated')
					return redirect('/studentp/')	
				else:
					error="Wrong Password"
					return render(request,'app/index.html',{'error':error})	#make all this as redirect instead of render
			except ObjectDoesNotExist:
				error="Wrong Id"
			return render(request,'app/index.html',{'error':error})
		else:
			error=type1
			try:
				q1=faculty.objects.get(id1=id1)
				if q1.password==password:
					request.session['f_logged'] = True
					request.session['f_id'] = q1.id
					return HttpResponse("Welcome Faculty")
					#return render(request,'app/faculty.html')	#Make this page
				else:
					error="Wrong Password"
					return render(request,'app/index.html',{'error':error})
			except ObjectDoesNotExist:
				error="Wrong Id"
			return render(request,'app/index.html',{'error':error})

	return render(request,'app/index.html',{'error':error})

def studentp(request):
	if request.session['s_logged']==True:
		pk1=request.session['s_id']
		q=student.objects.get(id=pk1)
		mess_dues=q.mess_dues
		mess_fees=q.mess_fees
		lib_dues=q.lib_dues
		reg_fees=q.reg_fees
		if request.method=="POST":
			type1=request.POST.get('type', '')
			if type1=="mess_dues":
				q.mess_dues=0
				q.save()
			if type1=="mess_fees":
				q.mess_fees=0
				q.save()
			if type1=="lib_dues":
				q.lib_dues=0
				q.save()
			if type1=="reg_fees":
				q.reg_fees=0
				q.save()
		if q.mess_dues==0 and q.mess_fees==0 and q.reg_fees==0 and q.lib_dues==0:
			messages.success(request,"All dues cleared and fees paid! You can register for courses now")
			request.session['money_paid'] = True
			redirect('/studentc')
		return render(request,'app/student.html',{'mess_dues':mess_dues,'mess_fees':mess_fees,'lib_dues':lib_dues,'reg_fees':reg_fees})
		#do something
	else:
		messages.success(request, 'Please Login First')
		return redirect('/')

def studentc(request):
	if request.session['money_paid']==True:
		
	else:
		messages.success(request, 'Complete your payment process to register for courses')
		return redirect('/studentp')

def logout_s(request):
	error=None
	if request.session['s_logged']==True:
		del request.session['s_logged']
		del request.session['s_id']
	else:
		error="Login First"
	return render(request,'app/index.html',{'error':error})

def logout_f(request):
	error=None
	if request.session['f_logged']==True:
		del request.session['f_logged']
		del request.session['f_id']
	else:
		error="Login First"
	return render(request,'app/index.html',{'error':error})
