from __future__ import unicode_literals

from django.db import models



class student(models.Model):
	name=models.CharField(max_length=30)
	id1=models.CharField(max_length=10)
	password=models.CharField(max_length=30)
	reg_done=models.IntegerField(default=0)
	semester=models.IntegerField(default=1)
	mess_dues=models.IntegerField(default=0)
	mess_fees=models.IntegerField(default=0)
	lib_dues=models.IntegerField(default=0)
	reg_fees=models.IntegerField(default=0)
	def __str__(self):
		a=self.name
		return a

class course(models.Model):
    name=models.CharField(max_length=30)
    code=models.CharField(max_length=10)
    #students=models.ManyToManyField(student,blank=True)
    faculty_name=models.CharField(max_length=30)
    note=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name

class faculty(models.Model):
	name=models.CharField(max_length=30)
	id1=models.CharField(max_length=10)
	password=models.CharField(max_length=30)
	#courses=models.ManyToManyField(course,blank=True)
	#request=models.ManyToManyField(student,blank=True)
	def __str__(self):
		return self.name