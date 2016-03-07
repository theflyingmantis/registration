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
	request.session['f_logged'] = False
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
					#return HttpResponse("Welcome Faculty")
					return redirect('/facultyp/')
					#return render(request,'app/faculty.html')	#Make this page
				else:
					error="Wrong Password"
					return render(request,'app/index.html',{'error':error})
			except ObjectDoesNotExist:
				error="Wrong Id"
			return render(request,'app/index.html',{'error':error})

	return render(request,'app/index.html',{'error':error})

def facultyp(request):
	if request.session['f_logged']==True:
		pk=request.session['f_id']
		fac=faculty.objects.get(pk=pk)
		requests=fac.requests.all()
		c = {}
		c.update(csrf(request))
		if request.method=="POST":
			type1=request.POST.get('type', '')
			id1=request.POST.get('name', '')
			cname=request.POST.get('cname', '')
			print id1+" "+cname
			if type1=="yes":
				q1=fulldetail.objects.get(id1=id1)
				c1=course.objects.get(name=cname)
				q1.courses.add(c1)
				q1.save()
				q2=request1.objects.get(id1=id1,course_name=cname)
				q2.delete()
			else:
				q2=request1.objects.get(id1=id1,course_name=cname)
				q2.delete()
			msg=request.POST.get('message','')
			if msg!='':
				sname=fac.name#Sender's Name
				n1=message(receiver=id1,sender=pk,msg=msg,sname=sname)
				n1.save()
			else:
				sname=fac.name
				msg1="Request Declined for Elective."
				n1=message(receiver=id1,sender=pk,msg=msg1,sname=sname)
				n1.save()
		return render(request,'app/facultyp.html',{'requests':requests})
	else:
		messages.success(request, 'Please Login First')
		return redirect('/')

def smessage(request):
	if request.session['s_logged']==True:
		pk1=request.session['s_id']
		q1=message.objects.filter(receiver=pk1)
		if request.method=="POST":
			sender=request.POST.get('sender', '')
			value=request.POST.get('msg_value','')
			q2=message.objects.filter(sender=sender,msg=value)
			q2.delete()
		return render(request,'app/smessage.html',{'msgs':q1})
	else:
		messages.success(request, 'Please Login First')
		return redirect('/')

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
		c = {}	
		c.update(csrf(request))
		courses=course.objects.all()
		pk1=request.session['s_id']
		q=student.objects.get(id=pk1)
		q1=compulsary.objects.get(branch=q.branch)
		sem=q.semester
		if sem==1:
			c_courses=q1.sem1
		if sem==2:
			c_courses=q1.sem2
		if sem==3:
			c_courses=q1.sem3
		if sem==4:
			c_courses=q1.sem4
		if sem==5:
			c_courses=q1.sem5
		if sem==6:
			c_courses=q1.sem6
		if sem==7:
			c_courses=q1.sem7
		if sem==8:
			c_courses=q1.sem8
		cm_courses=c_courses.all()
		#print cm_courses
		try:
			q2=fulldetail.objects.get(id1=pk1)
		except ObjectDoesNotExist:
			q2=fulldetail(id1=pk1)
		q2.name=q.name
		q2.branch=q.branch
		q2.email=q.email
		q2.semester=q.semester
		q2.save()
		for c in cm_courses:
			c1=course.objects.get(code=c.code)
			q2.courses.add(c1)
			q2.save()
		if request.method=="POST":
			code=request.POST.get('type', '')
			flag=True
			try:
				q3=request1.objects.get(id1=pk1,course_name=course.objects.get(code=code).name)
				messages.success(request,"Request already sent!")
			except ObjectDoesNotExist:
				for c in cm_courses:
					if c.code==code:
						flag=False
						messages.success(request,"This is a compulsary course. Already selected by default! Choose electives to send request")
				if flag==True:
					q=course.objects.get(code=code)
					cname=q.name
					fcode=q.faculty_code
					q1=faculty.objects.get(id1=fcode)
					sdetail=student.objects.get(id=pk1)
					a1=request1(id1=pk1,course_name=cname,name=sdetail.name,semester=sdetail.semester,branch=sdetail.branch,email=sdetail.email)	#Much more can be passed here !! Ajeet's object can be :P
					a1.save()
					q1.requests.add(a1)
					q1.save()
					messages.success(request,"Request sent!")
		return render(request,'app/student_registration.html',{'courses':courses,'cm_courses':cm_courses})
	else:
		messages.success(request, 'Complete your payment process to register for courses')
		return redirect('/studentp')

def logout_s(request):
	error=None
	if request.session['s_logged']==True:
		del request.session['s_logged']
		del request.session['s_id']
		messages.success(request,"Thanks for using portal!")
	else:
		messages.success(request,"Login first")
	return redirect('/')

def logout_f(request):
	error=None
	if request.session['f_logged']==True:
		del request.session['f_logged']
		del request.session['f_id']
		messages.success(request,"Thanks for using portal!")
	else:
		messages.success(request,"Login first")
	return redirect('/')
