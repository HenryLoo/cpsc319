from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings

def class_attendance(request):
	return render(request, 'school_components/class_attendance.html')

def class_grading(request):
	return render(request, 'school_components/class_grading.html')