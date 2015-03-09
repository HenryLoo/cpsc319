from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from assignment.models import Assignment

def view_assignment(request):
    return render(request, "school_components/view_assignment.html")
