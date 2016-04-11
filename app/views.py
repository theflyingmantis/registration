from django.shortcuts import render,render_to_response,redirect
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from app.models import *
from django.contrib import messages

def index(request):	#Base Url - Home page 
	c = {}
	error=None
	c.update(csrf(request))
	request.session['freeze']=False	
	request.session['accounts']=False				#Sessions Created
	request.session['admin_logged'] = False
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

def admin_login(request):	#To check for registered Students
	if request.method=="POST":
		name=request.POST.get('name', '')
		password=request.POST.get('password', '')
		if name=="admin" and password=="admin":
			request.session['admin_logged'] = True
			return redirect('/admin_settings')
		else:
			messages.success(request, 'Wrong Username/Password')
	return render(request,'app/admin_login.html')

def admin_settings(request):	#To check for registered Students
	if request.session['admin_logged'] == True:
		students=student.objects.filter(reg_done=1)
		return render(request,'app/admin_settings.html',{'students':students})
	else:
		messages.success(request, '@ Admin. Please Login first to authenticate yourself !')
		return redirect('/')


def facultyp(request):	#Faculty Elective request
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
			print "tmp : " + request.POST.get('tmp', '')
			# print id1+" "+cname
			# print type1
			msg=request.POST.get('message','')
			if type1=="on":
				print "YES is there"
				try:
					q1=fulldetail.objects.get(id1=id1)
					c1=course.objects.get(name=cname)
					q1.courses.add(c1)
					q1.save()
					q2=request1.objects.get(id1=id1,course_name=cname)
					q2.delete()
				except ObjectDoesNotExist:
					q2=request1.objects.get(id1=id1,course_name=cname)
					q2.delete()
			else:
				print "NO is there"
				q2=request1.objects.get(id1=id1,course_name=cname)
				q2.delete()
				#c1=course.objects.get(name=cname)
				if msg=='':
					sname=fac.name#Sender's Name
					msg1="Request Declined"
					n1=message(receiver=id1,sender=pk,msg=msg1,sname=sname)
					n1.save()
			
			print "msg: " + msg
			if msg!='':
				sname=fac.name#Sender's Name
				n1=message(receiver=id1,sender=pk,msg=msg,sname=sname)
				n1.save()
			# else:
			# 	sname=fac.name
			# 	msg1="Request Declined for Elective."#***********************************DOUBT...why so
			# 	n1=message(receiver=id1,sender=pk,msg=msg1,sname=sname)
			# 	n1.save()
		return render(request,'app/facultyp.html',{'requests':requests,'fac':fac.name})
	else:
		messages.success(request, 'Please Login First')
		return redirect('/')

def student_course(request):	#Displays students in particular course
	if request.session['f_logged']==True:
		pk=request.session['f_id']
		fac=faculty.objects.get(pk=pk)
		c1=fac.courses.all()
		print c1
		return render(request,'app/student_course.html',{'courses':c1,'fac':fac})

	else:
		messages.success(request, 'Please Login First')
		return redirect('/')
		
def StudentsInCourse(request,name):	#Display PArticular Student	
	if request.session['f_logged']==True:
		pk=request.session['f_id']
		fac=faculty.objects.get(pk=pk)
		crs=course.objects.get(code=name)
		students=crs.students.all()
		return render(request,'app/StudentsInCourses.html',{'fac':fac,'students':students})
	else:
		messages.success(request, 'Please Login First')
		return redirect('/')


def facultyc(request):	#Faculty Mentor Request
	if request.session['f_logged']==True:
		pk=request.session['f_id']
		fac=faculty.objects.get(pk=pk)
		m_request=fac.fulldetails.all()
		return render(request,'app/facultyc.html',{'fac':fac,'requests':m_request})
	else:
		messages.success(request, 'Please Login First')
		return redirect('/')


def ffinal(request,id1):	#Faculty Mentor Request
	if request.session['f_logged']==True:
		pk=request.session['f_id']
		fac=faculty.objects.get(pk=pk)
		s1=student.objects.get(pk=id1)
		q2=fulldetail.objects.get(id1=id1)
		q3=q2.courses.all()
		if request.method=="POST":
			type1=request.POST.get('type', '')
			msg=request.POST.get('msg_mentor','')
			if type1=='on':
				d1=final_fulldetail(id1=q2.id1)
				d1.save()
				for c in q3:
					d1.courses.add(c)
				d1.save()
				s1.reg_done=1
				s1.save()
				for c in q3:
					c.students.add(s1)
				q2.delete()
			else:
				q2.delete()
			if msg!='':
				n1=message(receiver=id1,sender=pk,msg=msg,sname=fac.name)
				n1.save()
			messages.success(request,'Status submitted.')
			return redirect('/facultyc')

		return render(request,'app/ffinal.html',{'student':s1,'fac':fac,'courses':q3})
	else:
		messages.success(request, 'Please Login First')
		return redirect('/')

def smessage(request):	#Shows messages of students
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

def studentp(request):	#Student Payment Portal
	if request.session['s_logged']==True:
		pk1=request.session['s_id']
		q=student.objects.get(id=pk1)
		mess_dues=q.mess_dues
		mess_fees=q.mess_fees
		lib_dues=q.lib_dues
		reg_fees=q.reg_fees
		if request.method=="POST":
			type1=request.POST.get('type', '')
			debitcard=request.POST.get('debitcard','')
			if type1=="mess_dues" and q.mess_dues!=0:
				n1=accounts(name=q.name,roll=q.id1,typefees="Mess Dues",amount=mess_dues,cardno=debitcard)
				n1.save()
				q.mess_dues=0
				q.save()
			if type1=="mess_fees" and q.mess_fees!=0:
				n1=accounts(name=q.name,roll=q.id1,typefees="Mess Fees",amount=mess_fees,cardno=debitcard)
				n1.save()
				q.mess_fees=0
				q.save()
			if type1=="lib_dues" and q.lib_dues!=0:
				n1=accounts(name=q.name,roll=q.id1,typefees="Library Dues",amount=lib_dues,cardno=debitcard)
				n1.save()
				q.lib_dues=0
				q.save()
			if type1=="reg_fees" and q.reg_fees!=0:
				n1=accounts(name=q.name,roll=q.id1,typefees="Registration Fees",amount=reg_fees,cardno=debitcard)
				n1.save()
				q.reg_fees=0
				q.save()
		if q.mess_dues==0 and q.mess_fees==0 and q.reg_fees==0 and q.lib_dues==0:
			messages.success(request,"All dues cleared and fees paid! You can register for courses now.")
			request.session['money_paid'] = True
			redirect('/studentc')
		return render(request,'app/student.html',{'student':q,'mess_dues':mess_dues,'mess_fees':mess_fees,'lib_dues':lib_dues,'reg_fees':reg_fees})
		#do something
	else:
		messages.success(request, 'Please Login First')
		return redirect('/')



def studentc(request):	#Student Registration Courses
	if request.session['money_paid']==True and request.session['freeze']==False:
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
			type1=request.POST.get('type1','')
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


def sfinal(request):	#Final Page to be printed
	if request.session['money_paid']==True and request.session['freeze']==False:	#add here if registration is complete. If yes - redirect to other page
		id1=request.session['s_id']
		
		s1=student.objects.get(pk=id1)
		if s1.reg_done==1:
			return redirect('/confirmed')
		sem=s1.semester
		q1=branch_mentor.objects.get(branch=s1.branch)
		
		if sem==1:
			mentor=q1.sem1
		if sem==2:
			mentor=q1.sem2
		if sem==3:
			mentor=q1.sem3
		if sem==4:
			mentor=q1.sem4
		if sem==5:
			mentor=q1.sem5
		if sem==6:
			mentor=q1.sem6
		if sem==7:
			mentor=q1.sem7
		if sem==8:
			mentor=q1.sem8
		mentor1=mentor.all()
		try:
			q2=fulldetail.objects.get(id1=id1)
		except ObjectDoesNotExist:
			messages.success(request,"Your request was Rejected by Faculty Mentor. Register Again!")
			return redirect('/studentc')
		q3=q2.courses.all()
		if request.method=="POST":
			messages.success(request,"Request sent to Faculty Advisor")
			f1=faculty.objects.get(id1=mentor1[0].id1)
			f1.fulldetails.add(q2)
		return render(request,'app/sfinal.html',{'courses':q3,'mentor':mentor1[0]})
	else:
		messages.success(request, 'Complete your payment process to register for courses')
		return redirect('/studentp')

def confirmed(request):	#If confirmed - Show final page
	if request.session['money_paid']==True:
		id1=request.session['s_id']
		s1=student.objects.get(pk=id1)
		sem=s1.semester
		q1=branch_mentor.objects.get(branch=s1.branch)
		
		if sem==1:
			mentor=q1.sem1
		if sem==2:
			mentor=q1.sem2
		if sem==3:
			mentor=q1.sem3
		if sem==4:
			mentor=q1.sem4
		if sem==5:
			mentor=q1.sem5
		if sem==6:
			mentor=q1.sem6
		if sem==7:
			mentor=q1.sem7
		if sem==8:
			mentor=q1.sem8
		mentor1=mentor.all()
		q2=final_fulldetail.objects.get(id1=id1)
		q3=q2.courses.all()
		return render(request,'app/reg_complete.html',{'student':s1,'courses':q3,'mentor':mentor1[0]})
	else:
		messages.success(request, 'Complete your payment process first')
		return redirect('/studentp')


def logout_a(request):	#logout Admin
	error=None
	if request.session['a_logged']==True:
		del request.session['a_logged']
		messages.success(request,"Thanks for using portal!")
	else:
		messages.success(request,"Login first")
	return redirect('/')


def logout_s(request):	#logout Student
	error=None
	if request.session['s_logged']==True:
		del request.session['s_logged']
		del request.session['s_id']
		messages.success(request,"Thanks for using portal!")
	else:
		messages.success(request,"Login first")
	return redirect('/')

def logout_f(request):	#logout Faculty
	error=None
	if request.session['f_logged']==True:
		del request.session['f_logged']
		del request.session['f_id']
		messages.success(request,"Thanks for using portal!")
	else:
		messages.success(request,"Login first")
	return redirect('/')

def course_info(request):	#info about particular course
	crs=course.objects.all()
	return render(request,"app/course_info.html",{'courses':crs})

def timetable(request):
	return render(request,'app/timetable.html')

def accounts_login(request):
	if request.method=="POST":
		username=request.POST.get('name', '')
		password=request.POST.get('pass','')
		if username=="accounts" and password=="pass":
			request.session['accounts']=True
			return redirect('/accounts_details')
		else:
			messages.success(request,"Wrong Credentials")
		#do something
	return render(request,'app/accounts_login.html')

def accounts_logout(request):
	if request.session['accounts']==True:
		del request.session['accounts']
		#del request.session['f_id']
		messages.success(request,"Thanks for using portal!")
	else:
		messages.success(request,"Login first")
	return redirect('/')

def  accounts_details(request):
	if request.session['accounts']==True:
		acc=accounts.objects.all()
		print acc
		return render(request,'app/accounts_details.html',{'accounts':acc})
	else:
		messages.success(request,"Login first")
		return redirect('/')


def fee_structure(request):
	return render(request,'app/fee_structure.html')