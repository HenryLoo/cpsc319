from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.shortcuts import render_to_response
from django.http import HttpResponse
from reports.models import Reports


def view_reports(request):
    return render(request, "reports/view_reports.html")

def create_new_report_page(request):
    return render(request, "reports/create_new_report_page.html")
