from __future__ import unicode_literals

from django.db import models
from app.models import *
from django import forms

REG_DONE= [(0, 'No'), (1, 'Yes')]
SEMESTER= [(1, '1st'), (2, '2nd'), (3, '3rd'), (4, '4th'), (5, '5th'), (6, '6th'), (7, '7th'), (8, '8th')]
COURSE= [('cse', 'Computer Science & Engineering'), ('ele', 'Electrical Engineering'), ('mech', 'Mechanical Engineering')]
class student(models.Model):		#Base Class Student which contains all details about student 1
	name=models.CharField(max_length=30)
	email=models.EmailField(max_length=30,null=True)
	id1=models.CharField(max_length=10,help_text="This is LDAP id")
	password=models.CharField(max_length=30,help_text="This is LDAP password")
	reg_done=models.IntegerField(default=0,choices=REG_DONE)
	semester=models.PositiveIntegerField(default='1st',choices=SEMESTER)
	branch=models.CharField(max_length=30,null=True,choices=COURSE)		
	mess_dues=models.PositiveIntegerField(default=0)
	mess_fees=models.PositiveIntegerField(default=0)
	lib_dues=models.PositiveIntegerField(default=0)
	reg_fees=models.PositiveIntegerField(default=0)
	def __str__(self):
		a=self.name
		return a

class message(models.Model):	#Stores Message
	receiver=models.CharField(max_length=30)
	sender=models.CharField(max_length=30)
	sname=models.CharField(max_length=30,blank=True)
	msg=models.CharField(max_length=1000)
	def __str__(self):
		return self.msg+" "+self.sname

class accounts(models.Model):	#stores accounts data
	name=models.CharField(max_length=30)
	roll=models.CharField(max_length=30)
	typefees=models.CharField(max_length=30)
	amount=models.PositiveIntegerField()
	cardno=models.BigIntegerField(default=0)
	def __str__(self):
		a=self.name+" "+self.typefees
		return a

class course(models.Model):	#Stores Course
    name=models.CharField(max_length=30)
    code=models.CharField(max_length=10,help_text="Course Code. \nExample : CS221")
    students=models.ManyToManyField(student,blank=True)
    faculty_code=models.CharField(max_length=10,null=True)		
    faculty_name=models.CharField(max_length=30)
    note=models.CharField(max_length=100,null=True)
    ltp=models.CharField(max_length=10,null=True,help_text="Enter in the form L-T-P [credit]     Example: 3-0-3 [4]\n")
    def __str__(self):
        return self.name

class fulldetail(models.Model):	#As Temporary Model
	id1=models.IntegerField()
	name=models.CharField(max_length=30,null=True)
	semester=models.IntegerField(null=True)
	branch=models.CharField(max_length=10,null=True)
	courses=models.ManyToManyField(course,blank=True)
	def __str__(self):
		name=student.objects.get(pk=self.id1)
		return name.name


class final_fulldetail(models.Model):	#Final Database record for courses of a student
	id1=models.IntegerField()
	courses=models.ManyToManyField(course,blank=True)
	def __str__(self):
		name=student.objects.get(pk=self.id1)
		return name.name

class request1(models.Model):	#database of request
    id1=models.IntegerField() #student pk
    name=models.CharField(max_length=30,null=True)
    semester=models.PositiveIntegerField(null=True)
    branch=models.CharField(max_length=10,null=True)
    email=models.CharField(max_length=30,null=True)
    course_name=models.CharField(max_length=30)
    ctype=models.CharField(max_length=30,null=True)
    def __str__(self):
    	name=student.objects.get(pk=self.id1)
    	return name.name+" * "+self.course_name

class faculty(models.Model):	#Faculty Database
	name=models.CharField(max_length=30)
	mentor=models.BooleanField(default=False)
	id1=models.CharField(max_length=10)
	password=models.CharField(max_length=30)
	courses=models.ManyToManyField(course,blank=True)
	requests=models.ManyToManyField(request1,blank=True)
	fulldetails=models.ManyToManyField(fulldetail,blank=True)
	def __str__(self):
		return self.name


class branch_mentor(models.Model):	#Stores Branch mentor per semester
 	branch=models.CharField(max_length=10)
 	sem1=models.ManyToManyField(faculty,related_name='sem1',blank=True)
 	sem2=models.ManyToManyField(faculty,related_name='sem2',blank=True)
 	sem3=models.ManyToManyField(faculty,related_name='sem3',blank=True)
 	sem4=models.ManyToManyField(faculty,related_name='sem4',blank=True)
 	sem5=models.ManyToManyField(faculty,related_name='sem5',blank=True)
 	sem6=models.ManyToManyField(faculty,related_name='sem6',blank=True)
 	sem7=models.ManyToManyField(faculty,related_name='sem7',blank=True)
 	sem8=models.ManyToManyField(faculty,related_name='sem8',blank=True)
	def __str__(self):
		return self.branch+"- mentor"
 
class compulsary(models.Model):	#Compulsary Courses
 	branch=models.CharField(max_length=10)
 	sem1=models.ManyToManyField(course,related_name='sem1',blank=True)
 	sem2=models.ManyToManyField(course,related_name='sem2',blank=True)
 	sem3=models.ManyToManyField(course,related_name='sem3',blank=True)
 	sem4=models.ManyToManyField(course,related_name='sem4',blank=True)
 	sem5=models.ManyToManyField(course,related_name='sem5',blank=True)
 	sem6=models.ManyToManyField(course,related_name='sem6',blank=True)
 	sem7=models.ManyToManyField(course,related_name='sem7',blank=True)
 	sem8=models.ManyToManyField(course,related_name='sem8',blank=True)
 	def __str__(self):
 		return self.branch+"- compulsary courses"
