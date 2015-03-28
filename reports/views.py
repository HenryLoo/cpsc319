from django.shortcuts import render
from reportlab.pdfgen import canvas
from django.shortcuts import render_to_response
from django.http import HttpResponse
from reports.models import Reports


def view_reports(request):
    return render(request, "reports/view_reports.html")

def reportcard_teacher(request):
    return render(request, "reports/reportcard_teacher.html")

def create_new_report_page(request):
    return render(request, "reports/create_new_report_page.html")

def student_pdf(c):
    c.drawString(100, 100, "Hello World")
    c = canvas.Canvas("student.pdf")
    student_pdf(c)
    c.showPage()
    c.save()
