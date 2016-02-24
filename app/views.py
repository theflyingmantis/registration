from django.shortcuts import render,render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from app.models import *

def index(request):
	c = {}
	error=None
	c.update(csrf(request))
	if request.method=="POST":
		id1= request.POST.get('id', '')
		password = request.POST.get('password', '')
		type1=request.POST.get('type', '')
		
		if type1=='student':
			try:
				q=student.objects.get(id1=id1)
				if q.password==password:
					request.session['s_logged'] = True
					request.session['s_id'] = id1
					#return render(request,'app/student.html')	#Make this page
					return HttpResponse("Welcome Student")
				else:
					error="Wrong Password"
					return render(request,'app/index.html',{'error':error})
			except ObjectDoesNotExist:
				error="Wrong Id"
			return render(request,'app/index.html',{'error':error})
		else:
			error=type1
			try:
				q1=faculty.objects.get(id1=id1)
				if q1.password==password:
					request.session['f_logged'] = True
					request.session['f_id'] = id1
					return HttpResponse("Welcome Faculty")
					#return render(request,'app/faculty.html')	#Make this page
				else:
					error="Wrong Password"
					return render(request,'app/index.html',{'error':error})
			except ObjectDoesNotExist:
				error="Wrong Id"
			return render(request,'app/index.html',{'error':error})

	return render(request,'app/index.html',{'error':error})